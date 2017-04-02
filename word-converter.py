#!/usr/bin/env python
# coding=utf-8
import os

from misc import get_absolute_path

def polish_content(content):
    replace_dict = {
        '「': '“',
        '」': '”',
        '远': '遠',
        '杂': '雜',
        '敌': '敵',
        '杀': '殺',
        '虑': '慮',
        '叽': '嘰',
        '耸': '聳',
        '稳': '穩',
        '迟': '遲',
        '艳': '艷',
        '迈': '邁',
        '鉴': '鑒',
    }
    for ori_word, new_word in replace_dict.items():
        content = content.replace(ori_word, new_word)
    return content

def main():
    input_dir = '~/novels/tmpNovels/'
    output_dir = '~/novels/downloads'
    input_path = get_absolute_path(input_dir)
    output_path = get_absolute_path(output_dir)

    for file in os.listdir(input_path):
        file_path = os.path.join(input_path, file)
        output_file_path = os.path.join(output_path, file)
        article = ''
        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                for line in f.readlines():
                    article += line
            article = polish_content(article)
            with open(output_file_path, 'w') as f:
                f.write(article)


if __name__ == '__main__':
    main()
