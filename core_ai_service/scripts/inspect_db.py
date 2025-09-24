import sqlite3
import os

# --- CẤU H-I-N-H ---
DB_PATH = "./core_ai_service/data/Chinook_Sqlite.sqlite"
OUTPUT_DIR = "./core_ai_service/data"
OUTPUT_FILENAME = "database_schema_and_sample_data.txt"

def inspect_database_schema(db_path, output_file_path):
    """
    Kết nối tới một database SQLite, lấy cấu trúc và 5 dòng dữ liệu mẫu
    từ mỗi bảng, sau đó lưu kết quả vào một file text.
    """
    if not os.path.exists(db_path):
        print(f"Lỗi: Không tìm thấy file database tại '{db_path}'")
        return

    # Mở file để ghi kết quả
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(f"--- Bắt đầu kiểm tra cấu trúc database: {os.path.basename(db_path)} ---\n\n")
        
        try:
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row # Giúp truy cập cột bằng tên
            cursor = conn.cursor()

            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            if not tables:
                f.write("Database này không có bảng nào.\n")
                return

            f.write(f"Tìm thấy {len(tables)} bảng:\n\n")

            for table_name_tuple in tables:
                table_name = table_name_tuple[0]
                f.write(f"--- Bảng: {table_name} ---\n")

                # 1. In cấu trúc bảng
                f.write("Cấu trúc bảng:\n")
                cursor.execute(f"PRAGMA table_info('{table_name}');")
                columns = cursor.fetchall()
                
                f.write(f"{'Tên Cột':<25} {'Kiểu Dữ Liệu':<15} {'Cho phép NULL':<15} {'Khóa Chính':<10}\n")
                f.write("-" * 70 + "\n")
                
                column_names = []
                for col in columns:
                    column_names.append(col['name'])
                    not_null = "Không" if col['notnull'] == 1 else "Có"
                    is_pk = "Có" if col['pk'] == 1 else ""
                    f.write(f"{col['name']:<25} {col['type']:<15} {not_null:<15} {is_pk:<10}\n")
                
                f.write("\n")

                # 2. In 5 dòng dữ liệu mẫu
                f.write("5 dòng dữ liệu mẫu:\n")
                try:
                    cursor.execute(f'SELECT * FROM "{table_name}" LIMIT 5;')
                    sample_rows = cursor.fetchall()

                    if not sample_rows:
                        f.write("Bảng này không có dữ liệu.\n")
                    else:
                        header = " | ".join(column_names)
                        f.write(header + "\n")
                        f.write("-" * len(header) + "\n")
                        for row in sample_rows:
                            row_values = [str(row[col_name]) for col_name in column_names]
                            f.write(" | ".join(row_values) + "\n")
                except Exception as e:
                     f.write(f"Không thể lấy dữ liệu mẫu: {e}\n")

                f.write("\n" + "="*80 + "\n\n")

        except sqlite3.Error as e:
            f.write(f"Lỗi khi truy cập database: {e}\n")
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    print(f"Kiểm tra hoàn tất. Kết quả đã được lưu tại: {output_file_path}")

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    output_file_path = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)
    inspect_database_schema(DB_PATH, output_file_path)