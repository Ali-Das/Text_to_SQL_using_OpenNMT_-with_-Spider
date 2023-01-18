from __future__ import unicode_literals, print_function, division
from onmt.library.query import Query
import pandas as pd
import nltk
import difflib
nltk.download('punkt')
  
class SqlGenUtil:
    """Class is responsible for converting output of NMT model to sql queries"""

    def __init__(self):
        pass

    def build_sql_from_txt(self, txtfile, dbfile, sqlfile):
        tables = pd.read_json(dbfile, lines=True)
        # iterate over the queries and convert each one to plain text sql
        ftext = open(txtfile, "r", encoding="utf-8")
        fsql = open(sqlfile, "w+", encoding="utf-8")
        ftext_contents = ftext.readlines()
      
        for line in ftext_contents:
            
            col_headers = []
            start = end = 0
            tokens = nltk.word_tokenize(line)
            line = ' '.join(str(word) for word in tokens)
            for token in tokens:
                if token == 'FROM':
                    start = tokens.index('FROM')
                elif token == 'WHERE':
                    end = tokens.index('WHERE')
            if line.find('WHERE') == -1:
                end = len(tokens)
            title = tokens[(start + 1): end]
            title_string = ' '.join(str(word) for word in title)
            table_name = "table_"
            for indx, ln in tables.iterrows():
                tbl_title = str(ln["page_title"])
                tkn = nltk.word_tokenize(tbl_title)
                table_title = ' '.join(tkn)
                if title_string.lower() == table_title.lower():
                    table_id = ln["id"]
                    table_id = str(table_id).replace("-", "_")
                    table_name += table_id
                    col_headers = ln["header"]
                    line = line.replace(title_string, str(table_name))
                    break
            indx = 0
            for item in col_headers:
                tkn = nltk.word_tokenize(item)
                header = ' '.join(tkn)
                col_headers[indx] = header
                indx += 1
            tokens = nltk.word_tokenize(line)
            column = 'col'
            for size_of_substring in range(8, 1, -1):
                substring_list = list(self.divide_chunks(tokens, size_of_substring))
                for l in substring_list:
                    substring_string = ' '.join(str(word) for word in l)
                    for item in col_headers:
                        if substring_string.lower() == str(item).lower():
                            col = column + str(col_headers.index(item))
                            line = line.replace(substring_string, col)
                        else:
                            substr = substring_string.replace(" ", "")
                            itm = str(item).replace(" ", "")
                            if substr.lower() == itm.lower():
                                col = column + str(col_headers.index(item))
                                line = line.replace(substring_string, col)
            for token in tokens:
                for item in col_headers:
                    if token.lower() == str(item).lower():
                        col = column + str(col_headers.index(item))
                        line = line.replace(token, col)

            query = " "
            indx = 0
            op = ['EQL', 'LT', 'LE', 'GT', 'GE']
            flag = 0
            tokens = nltk.word_tokenize(line)
    
            for token in tokens:
              if (indx + 1) == len(tokens):
                break
              else:   
                if token == 'LT':
                    query += ' <'
                elif token == 'LE':
                    query += ' <='
                elif token == 'GT':
                    query += ' >'
                elif token == 'GE':
                    query += ' ?='
                elif token == 'NE':
                    query += ' !='
                elif token == 'EQL':
                    query += ' ='
                    indx = tokens.index('EQL')
                    if (indx + 2) == len(tokens):
                        if str(tokens[indx + 1]).isalpha():
                            query += " \""
                            query += tokens[indx + 1]
                            query += "\""
                            break
                        elif str(tokens[indx + 1]).isdigit():
                            query += " "
                            query += tokens[indx + 1]
                            break
                        else:
                            if str(tokens[indx + 1]).find(',') != -1:
                                tokens[indx + 1] = str(tokens[indx + 1]).replace(",", "")
                                query += " "
                                query += tokens[indx + 1]
                                break
                            elif str(tokens[indx + 1]).find('.') != -1:
                                query += " "
                                query += tokens[indx + 1]
                                break
                            else:
                                query += " \""
                                query += tokens[indx + 1]
                                query += "\""
                                break
                    else:
                        if (indx + 1) == len(tokens):
                            break
                        elif str(tokens[indx + 1]).isalpha():
                            flag = 1
                            query += " \""
                        elif (str(tokens[indx + 2]) != 'AND') and (str(tokens[indx + 2]) != 'OR'):
                            flag = 1
                            query += " \""
                        elif str(tokens[indx + 1]).isdigit():
                            if str(tokens[indx + 1]).find(',') != -1:
                                tokens[indx + 1] = str(tokens[indx + 1]).replace(",", "")
                                query += " "
                                query += tokens[indx + 1]
                        else:
                            if str(tokens[indx + 1]).find('.') != -1:
                                query += " "
                                query += tokens[indx + 1]
                            else:
                                for o in ["-", "_", ":", "\\", "/", "%"]:
                                    if str(tokens[indx + 1]).find(o) != -1:
                                        flag = 1
                                        query += " \""
                elif token == 'AND' or token == 'OR':
                    if flag == 1:
                        query += "\""
                        flag = 0
                    query += " "
                    query += token
                else:
                    if flag == 1 and tokens.index(token) == (indx + 1):
                        query += token
                    else:
                        query += " "
                        query += token
            if flag == 1:
                query += "\""
                flag = 0
            
            query = query.replace('FROM', "as result FROM")
            if query.find("= \" ") != -1:
                query = query.replace("= \" ", "= \"").strip()
            else:
                query = query.strip()
            
            fsql.write(query)
            fsql.write("\n")
        ftext.close()
        fsql.close()

    def divide_chunks(self, tokens, size):
        # Yield successive size-sized chunks from list.
        for i in range(0, len(tokens) - 1):
            j = i + size
            yield tokens[i:j]
