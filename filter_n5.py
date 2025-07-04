#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv

def filter_n5_data():
    """
    从 notes.csv 文件中过滤第一列为 NEW-JLPT::NEW-N5 的行，
    并将结果输出到 n5.csv 文件中。
    """
    input_file = 'NEW-JLPT/notes.csv'
    output_file = 'n5.csv'
    target_deck = 'NEW-JLPT::NEW-N5'
    
    try:
        with open(input_file, 'r', encoding='utf-8') as infile, \
             open(output_file, 'w', encoding='utf-8', newline='') as outfile:
            
            csv_reader = csv.reader(infile)
            csv_writer = csv.writer(outfile)
            
            n5_count = 0
            
            for row in csv_reader:
                # 检查第一列是否为目标值
                if row and row[0] == target_deck:
                    csv_writer.writerow(row)
                    n5_count += 1
            
            print(f"成功过滤了 {n5_count} 条 N5 记录")
            print(f"结果已保存到 {output_file}")
            
    except FileNotFoundError:
        print(f"错误：找不到文件 {input_file}")
    except Exception as e:
        print(f"处理过程中发生错误：{e}")

if __name__ == "__main__":
    filter_n5_data() 