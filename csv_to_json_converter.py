#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV to JSON Converter for N5 Japanese Learning Data
Converts n5_extracted_v2.csv to JSON format with specified column mappings.
"""

import csv
import json
import sys
from pathlib import Path

def convert_csv_to_json(csv_file_path, output_file_path=None):
    """
    Convert CSV file to JSON format.
    
    Args:
        csv_file_path (str): Path to the input CSV file
        output_file_path (str, optional): Path for output JSON file. 
                                        If None, uses input filename with .json extension
    
    Returns:
        list: The converted data as a list of dictionaries
    """
    
    # Set default output file path if not provided
    if output_file_path is None:
        csv_path = Path(csv_file_path)
        output_file_path = csv_path.with_suffix('.json')
    
    data = []
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            
            # Skip header row (contains column letters)
            next(csv_reader)
            
            for row_num, row in enumerate(csv_reader, start=2):
                # Ensure row has enough columns (pad with empty strings if needed)
                while len(row) < 13:
                    row.append('')
                
                # Map columns according to user specification
                record = {
                    "id": row[0],                           # Column 1: ID
                    "word": row[1],                         # Column 2: 单词 (Japanese word)
                    "chinese_translation": row[2],          # Column 3: 中文翻译 (Chinese translation)
                    "japanese_pronunciation_file": row[3],  # Column 4: 日文的发音文件 (Japanese pronunciation file)
                    "example_sentence_1": row[4],           # Column 5: 日文的例句1 (Japanese example sentence 1)
                    "example_1_chinese_translation": row[5], # Column 6: 例句1的中文翻译 (Example sentence 1 Chinese translation)
                    "example_1_japanese_pronunciation": row[6], # Column 7: 例句1的日文发音 (Example sentence 1 Japanese pronunciation)
                    "example_sentence_2": row[7],           # Column 8: 日文的例句2 (Japanese example sentence 2)
                    "example_2_chinese_translation": row[8], # Column 9: 例句2的中文翻译 (Example sentence 2 Chinese translation)
                    "example_2_japanese_pronunciation": row[9], # Column 10: 例句2的日文发音 (Example sentence 2 Japanese pronunciation)
                    "example_sentence_3": row[10],          # Column 11: 日文的例句3 (Japanese example sentence 3)
                    "example_3_chinese_translation": row[11], # Column 12: 例句3的中文翻译 (Example sentence 3 Chinese translation)
                    "example_3_japanese_pronunciation": row[12] # Column 13: 例句3的日文发音 (Example sentence 3 Japanese pronunciation)
                }
                
                data.append(record)
                
        # Write to JSON file
        with open(output_file_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False, indent=2)
        
        print(f"✅ 转换成功！")
        print(f"📁 输入文件: {csv_file_path}")
        print(f"📁 输出文件: {output_file_path}")
        print(f"📊 转换了 {len(data)} 条记录")
        
        return data
        
    except FileNotFoundError:
        print(f"❌ 错误：找不到文件 {csv_file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 转换过程中出现错误: {str(e)}")
        sys.exit(1)

def main():
    """Main function to run the conversion."""
    
    # Default input file
    csv_file = "n5_extracted_v2.csv"
    
    # Check if file exists
    if not Path(csv_file).exists():
        print(f"❌ 错误：找不到文件 {csv_file}")
        print("请确保 n5_extracted_v2.csv 文件在当前目录中")
        sys.exit(1)
    
    # Convert CSV to JSON
    print("🚀 开始转换 CSV 到 JSON...")
    data = convert_csv_to_json(csv_file)
    
    # Display sample of converted data
    print("\n📋 转换数据样例:")
    if data:
        sample_record = data[0]
        for key, value in sample_record.items():
            if value:  # Only show non-empty fields
                print(f"  {key}: {value}")
    
    print("\n✨ 转换完成！")

if __name__ == "__main__":
    main() 