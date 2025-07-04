#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv

def extract_columns_from_n5():
    """
    从 n5.csv 文件中提取指定列的数据：
    - 基础列：C, G, J, L, N, P (索引 2, 6, 9, 11, 13, 15)
    - 条件1：如果Q列为空且R列不为空，则提取R, T, V列 (索引 16, 17, 19, 21)
    - 条件2：如果W列为空且X列不为空，则提取X, Z, AB列 (索引 22, 23, 25, 27)
    
    注意：CSV列索引从0开始，所以A=0, B=1, C=2, ...
    """
    input_file = 'n5.csv'
    output_file = 'n5_extracted.csv'
    
    # 定义列索引 (CSV中A=0, B=1, C=2, ...)
    base_columns = [2, 6, 9, 11, 13, 15]  # C, G, J, L, N, P
    condition1_columns = [16, 18, 20]      # R, T, V
    condition2_columns = [23, 25, 27]      # X, Z, AB
    
    try:
        with open(input_file, 'r', encoding='utf-8') as infile, \
             open(output_file, 'w', encoding='utf-8', newline='') as outfile:
            
            csv_reader = csv.reader(infile)
            csv_writer = csv.writer(outfile)
            
            # 写入表头
            headers = ['C', 'G', 'J', 'L', 'N', 'P']
            
            extracted_count = 0
            
            for row in csv_reader:
                if len(row) < 28:  # 确保行有足够的列
                    # 用空字符串填充缺失的列
                    row.extend([''] * (28 - len(row)))
                
                # 提取基础列 C, G, J, L, N, P
                extracted_row = []
                for col_idx in base_columns:
                    if col_idx < len(row):
                        extracted_row.append(row[col_idx])
                    else:
                        extracted_row.append('')
                
                # 检查条件1：Q列(索引16)为空且R列(索引17)不为空
                q_col = row[16] if len(row) > 16 else ''
                r_col = row[17] if len(row) > 17 else ''
                
                if not q_col.strip() and r_col.strip():
                    # 添加R, T, V列的数据
                    for col_idx in condition1_columns:
                        if col_idx < len(row):
                            extracted_row.append(row[col_idx])
                        else:
                            extracted_row.append('')
                    
                    # 更新表头（如果是第一行）
                    if extracted_count == 0:
                        headers.extend(['R', 'T', 'V'])
                
                # 检查条件2：W列(索引22)为空且X列(索引23)不为空
                w_col = row[22] if len(row) > 22 else ''
                x_col = row[23] if len(row) > 23 else ''
                
                if not w_col.strip() and x_col.strip():
                    # 添加X, Z, AB列的数据
                    for col_idx in condition2_columns:
                        if col_idx < len(row):
                            extracted_row.append(row[col_idx])
                        else:
                            extracted_row.append('')
                    
                    # 更新表头（如果是第一行）
                    if extracted_count == 0:
                        headers.extend(['X', 'Z', 'AB'])
                
                # 写入表头（只在第一行）
                if extracted_count == 0:
                    csv_writer.writerow(headers)
                
                # 写入提取的数据行
                csv_writer.writerow(extracted_row)
                extracted_count += 1
            
            print(f"成功提取了 {extracted_count} 行数据")
            print(f"结果已保存到 {output_file}")
            print(f"提取的列：{', '.join(headers)}")
            
    except FileNotFoundError:
        print(f"错误：找不到文件 {input_file}")
    except Exception as e:
        print(f"处理过程中发生错误：{e}")

def preview_data():
    """预览数据以便调试"""
    input_file = 'n5.csv'
    
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            csv_reader = csv.reader(infile)
            
            print("预览前3行数据的关键列：")
            for i, row in enumerate(csv_reader):
                if i >= 3:
                    break
                
                if len(row) < 28:
                    row.extend([''] * (28 - len(row)))
                
                print(f"\n第{i+1}行:")
                print(f"  C(2): '{row[2] if len(row) > 2 else ''}'")
                print(f"  Q(16): '{row[16] if len(row) > 16 else ''}'")
                print(f"  R(17): '{row[17] if len(row) > 17 else ''}'")
                print(f"  W(22): '{row[22] if len(row) > 22 else ''}'")
                print(f"  X(23): '{row[23] if len(row) > 23 else ''}'")
                
    except Exception as e:
        print(f"预览数据时发生错误：{e}")

if __name__ == "__main__":
    print("=== 预览数据 ===")
    preview_data()
    print("\n=== 提取列数据 ===")
    extract_columns_from_n5() 