import csv

class CsvGenerator:
    # CSVファイルに書き出すためのファイル名を指定する
    filename = 'output.csv'
    export_list = None

    def __init__(self):
        pass

    def set_export_list(self, export_list):
        self.export_list = export_list

    def call(self):
        # CSVファイルを書き出すためのファイルオブジェクトを開く
        with open(self.filename, 'w', newline='', encoding='utf-8') as f:
    
            # CSVファイルを書き出すためのWriterオブジェクトを作成する
            writer = csv.writer(f)
    
            # データをCSVファイルに書き出す
            for row in self.export_list:
                writer.writerow(row)