#!/usr/bin/env python3
"""기존 DB 스키마 분석"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def analyze_schema():
    print("Analyzing existing database schema...")
    print("=" * 60)
    
    try:
        conn = psycopg2.connect(
            host=os.getenv('DATABASE_HOST'),
            user=os.getenv('DATABASE_USER'),
            password=os.getenv('DATABASE_PASSWORD'),
            database=os.getenv('DATABASE_NAME'),
            port=os.getenv('DATABASE_PORT', 5432),
            sslmode='require'
        )
        
        cur = conn.cursor()
        
        # 1. 모든 스키마 목록
        cur.execute("""
            SELECT schema_name 
            FROM information_schema.schemata 
            WHERE schema_name NOT IN ('information_schema', 'pg_catalog', 'pg_toast')
            ORDER BY schema_name;
        """)
        schemas = cur.fetchall()
        print("SCHEMAS:")
        for schema in schemas:
            print(f"  - {schema[0]}")
        
        # 2. morning_dev 스키마의 테이블들
        print(f"\nTABLES IN morning_dev SCHEMA:")
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'morning_dev'
            ORDER BY table_name;
        """)
        tables = cur.fetchall()
        for table in tables:
            print(f"  - {table[0]}")
        
        # 3. daily_messages 테이블 찾기
        print(f"\nLOOKING FOR daily_messages TABLE:")
        cur.execute("""
            SELECT table_schema, table_name 
            FROM information_schema.tables 
            WHERE table_name = 'daily_messages'
            ORDER BY table_schema;
        """)
        daily_tables = cur.fetchall()
        if daily_tables:
            for schema, table in daily_tables:
                print(f"  FOUND: {schema}.{table}")
                
                # daily_messages 테이블 스키마 분석
                print(f"\n  SCHEMA FOR {schema}.{table}:")
                cur.execute("""
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns 
                    WHERE table_schema = %s AND table_name = %s
                    ORDER BY ordinal_position;
                """, (schema, table))
                columns = cur.fetchall()
                for col_name, data_type, nullable, default in columns:
                    print(f"    {col_name}: {data_type} ({'NULL' if nullable == 'YES' else 'NOT NULL'}) {f'DEFAULT {default}' if default else ''}")
                
                # 데이터 확인
                cur.execute(f"SELECT COUNT(*) FROM {schema}.{table}")
                count = cur.fetchone()[0]
                print(f"    TOTAL ROWS: {count}")
                
                if count > 0:
                    cur.execute(f"SELECT * FROM {schema}.{table} LIMIT 3")
                    sample_data = cur.fetchall()
                    print(f"    SAMPLE DATA:")
                    for i, row in enumerate(sample_data, 1):
                        print(f"      {i}. {row}")
        else:
            print("  NOT FOUND")
        
        # 4. 'message' 관련 모든 테이블 찾기
        print(f"\nALL TABLES CONTAINING 'message':")
        cur.execute("""
            SELECT table_schema, table_name 
            FROM information_schema.tables 
            WHERE table_name LIKE '%message%'
            ORDER BY table_schema, table_name;
        """)
        message_tables = cur.fetchall()
        for schema, table in message_tables:
            print(f"  - {schema}.{table}")
            
            # 각 테이블의 행 수 확인
            try:
                cur.execute(f"SELECT COUNT(*) FROM {schema}.{table}")
                count = cur.fetchone()[0]
                print(f"    ROWS: {count}")
            except Exception as e:
                print(f"    ERROR: {e}")
        
        conn.close()
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    analyze_schema()