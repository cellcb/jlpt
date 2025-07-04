#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv

def extract_columns_from_n5():
    """
    从 n5.csv 文件中提取指定列的数据：
    - 基础列：C, G, J, L, N, P (索引 2, 6, 9, 11, 13, 15)
    - 条件1：如果Q列为空且R列不为空，则提取R, T, V列 (索引 16, 18, 20)
    - 条件2：如果W列为空且X列不为空，则提取X, Z, AB列 (索引 22, 24, 26)
    
    注意：CSV列索引从0开始，所以A=0, B=1, C=2, ...
    """
    input_file = 'n5.csv'
    output_file = 'n5_extracted_v2.csv'
    
    # 定义列索引 (CSV中A=0, B=1, C=2, ...)
    base_columns = [1, 2, 6, 9, 11, 13, 15]  # B, C, G, J, L, N, P
    
    try:
        with open(input_file, 'r', encoding='utf-8') as infile, \
             open(output_file, 'w', encoding='utf-8', newline='') as outfile:
            
            csv_reader = csv.reader(infile)
            csv_writer = csv.writer(outfile)
            
            # 写入表头
            headers = ['B', 'C', 'G', 'J', 'L', 'N', 'P']
            condition1_found = False
            condition2_found = False
            
            all_rows = []
            
            for row in csv_reader:
                # 确保行有足够的列
                while len(row) < 30:
                    row.append('')
                
                # 提取基础列 C, G, J, L, N, P
                extracted_row = []
                for col_idx in base_columns:
                    extracted_row.append(row[col_idx] if col_idx < len(row) else '')
                
                # 检查条件1：Q列(索引16)为空且R列(索引17)不为空
                q_col = row[16].strip() if len(row) > 16 else ''
                r_col = row[17].strip() if len(row) > 17 else ''
                
                condition1_met = (not q_col and r_col)
                
                # 检查条件2：W列(索引22)为空且X列(索引23)不为空
                w_col = row[22].strip() if len(row) > 22 else ''
                x_col = row[23].strip() if len(row) > 23 else ''
                
                condition2_met = (not w_col and x_col)
                
                # 记录条件满足情况
                if condition1_met and not condition1_found:
                    condition1_found = True
                if condition2_met and not condition2_found:
                    condition2_found = True
                
                # 添加条件列数据
                if condition1_met:
                    # 添加R, T, V列的数据 (索引17, 19, 21)
                    extracted_row.extend([
                        row[17] if len(row) > 17 else '',  # R
                        row[19] if len(row) > 19 else '',  # T
                        row[21] if len(row) > 21 else ''   # V
                    ])
                else:
                    extracted_row.extend(['', '', ''])
                
                if condition2_met:
                    # 添加X, Z, AB列的数据 (索引23, 25, 27)
                    extracted_row.extend([
                        row[23] if len(row) > 23 else '',  # X
                        row[25] if len(row) > 25 else '',  # Z
                        row[27] if len(row) > 27 else ''   # AB
                    ])
                else:
                    extracted_row.extend(['', '', ''])
                
                all_rows.append((extracted_row, condition1_met, condition2_met))
            
            # 构建最终表头
            final_headers = ['B', 'C', 'G', 'J', 'L', 'N', 'P']
            if condition1_found:
                final_headers.extend(['R', 'T', 'V'])
            if condition2_found:
                final_headers.extend(['X', 'Z', 'AB'])
            
            # 写入表头
            csv_writer.writerow(final_headers)
            
            # 写入数据行
            condition1_count = 0
            condition2_count = 0
            
            for row_data, cond1_met, cond2_met in all_rows:
                # 构建最终行数据
                final_row = row_data[:7]  # 基础列
                
                if condition1_found:
                    if cond1_met:
                        final_row.extend(row_data[7:10])  # R, T, V
                        condition1_count += 1
                    else:
                        final_row.extend(['', '', ''])
                
                if condition2_found:
                    if cond2_met:
                        final_row.extend(row_data[10:13])  # X, Z, AB
                        condition2_count += 1
                    else:
                        final_row.extend(['', '', ''])
                
                csv_writer.writerow(final_row)
            
            print(f"成功提取了 {len(all_rows)} 行数据")
            print(f"结果已保存到 {output_file}")
            print(f"提取的列：{', '.join(final_headers)}")
            print(f"满足条件1的行数 (Q空且R不空): {condition1_count}")
            print(f"满足条件2的行数 (W空且X不空): {condition2_count}")
            
    except FileNotFoundError:
        print(f"错误：找不到文件 {input_file}")
    except Exception as e:
        print(f"处理过程中发生错误：{e}")

def analyze_conditions():
    """分析条件满足情况"""
    input_file = 'n5.csv'
    
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            csv_reader = csv.reader(infile)
            
            condition1_count = 0
            condition2_count = 0
            sample_condition1 = []
            sample_condition2 = []
            
            for i, row in enumerate(csv_reader):
                if i >= 873:  # 限制检查行数
                    break
                
                # 确保行有足够的列
                while len(row) < 30:
                    row.append('')
                
                # 检查条件1：Q列(索引16)为空且R列(索引17)不为空
                q_col = row[16].strip() if len(row) > 16 else ''
                r_col = row[17].strip() if len(row) > 17 else ''
                
                if not q_col and r_col:
                    condition1_count += 1
                    if len(sample_condition1) < 3:
                        sample_condition1.append(f"行{i+1}: Q='{q_col}', R='{r_col}'")
                
                # 检查条件2：W列(索引22)为空且X列(索引23)不为空
                w_col = row[22].strip() if len(row) > 22 else ''
                x_col = row[23].strip() if len(row) > 23 else ''
                
                if not w_col and x_col:
                    condition2_count += 1
                    if len(sample_condition2) < 3:
                        sample_condition2.append(f"行{i+1}: W='{w_col}', X='{x_col}'")
            
            print("=== 条件分析结果 ===")
            print(f"条件1 (Q空且R不空) 满足的行数: {condition1_count}")
            if sample_condition1:
                print("样例:")
                for sample in sample_condition1:
                    print(f"  {sample}")
            
            print(f"\n条件2 (W空且X不空) 满足的行数: {condition2_count}")
            if sample_condition2:
                print("样例:")
                for sample in sample_condition2:
                    print(f"  {sample}")
            
    except Exception as e:
        print(f"分析数据时发生错误：{e}")

if __name__ == "__main__":
    print("=== 分析条件 ===")
    analyze_conditions()
    print("\n=== 提取列数据 ===")
    extract_columns_from_n5() 