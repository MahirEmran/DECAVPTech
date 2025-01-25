import os
import os.path
import pdfplumber
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal, LTChar
def remove_blank_lines():
    for filename in os.listdir('output/'):
        # if filename == 'PF Area.txt':
        #     continue
        with open('output/' + filename, encoding='utf-8') as f:
            lines = f.readlines()
        result = []
        previous_blank = False
        for i in range(len(lines)):
            line = lines[i]
            if line.strip() == '':
                if not previous_blank and not lines[i+1].startswith("SOURCE"):
                    result.append(line)
                previous_blank = True
            else:
                result.append(line)
                previous_blank = False
        with open('output/' + filename, mode='w') as f:
            f.write('')
        with open('output/' + filename, mode='a', encoding='utf-8') as f2:
            for s in result:
                f2.write(s)


def organize_q_a():
    output = ""
    for filename in os.listdir('input/'):
        if exclude_file(filename):
            continue
        output_txt = []
        with open('input/' +filename, encoding='UTF8') as f:
            lines = f.readlines()
            print(filename)
            keyIndex = next(i for i, line in enumerate(lines) if 'KEY' in line.strip())

            firstQuestion = next(i for i, line in enumerate(lines) if line.strip().startswith('1.'))

            num = 1
            for i in range(firstQuestion, keyIndex):
                if num == 101:
                    break
                line = lines[i]
                question = ""
                ans = ""
                if line.startswith(f'{num}. ') and num < 101:
                    question = line.replace("\n", "") + " "
                    i += 1
                    while not lines[i].startswith('D.'):
                        if(not lines[i].startswith('Copyright © 2024 by MBA Research and Curriculum Center®, Columbus, Ohio') and not lines[i].startswith('Test') and not lines[i] == '\n'):
                            if not lines[i].startswith('D.') and not lines[i].startswith('C.') and not lines[i].startswith('B.') and not lines[i].startswith('A.'):
                                question += lines[i].replace("\n", "") + " "
                            else:
                                if lines[i].startswith("A."):
                                    question += "\n"
                                question += lines[i] 
                        i += 1
                    question += lines[i]
                    for j in range(keyIndex, len(lines)):
                        if lines[j].startswith(f'{num}.') and num < 101:
                            while j < len(lines) and (not lines[j].startswith(f'{num+1}. ')):
                                if(not lines[j].startswith('Copyright © 2024 by MBA Research and Curriculum Center®, Columbus, Ohio') and not lines[j].startswith('Test') and not lines[j] == '\n'):
                                    if lines[j].startswith("SOURCE"):
                                        ans += "\n" + lines[j] 
                                    elif lines[j].startswith(f'{num}.'):
                                        ans += lines[j]
                                    else:
                                        ans += lines[j].replace("\n", "") +" "
                                j+= 1
                
                    num += 1
                output_txt.append(question + "\n" + ans)

        if not os.path.isfile('output/' + filename):
            with open('output/' + filename, mode='x') as f2:
                f2.write("")
        with open('output/' + filename, mode='a', encoding='utf-8') as f2:
            for s in output_txt:
                f2.write(s)

def organize_instruct_areas():
    deca_codes = {
        'PM': 'Pricing',
        'PD': 'Product_Service Management',
        'MK': 'Marketing',
        'PI': 'Promotion',
        'IM': 'Information Management',
        'HR': 'Human Resources',
        'CM': 'Channel Management',
        'RM': 'Risk Management',
        'BL': 'Business Law',
        'CR': 'Customer Relations',
        'QM': 'Quality Management',
        'PJ': 'Project Management',
        'KM': 'Knowledge Management',
        'PR': 'Professional Development',
        'FM': 'Financial-Information Management',
        'SE': 'Selling',
        'MP': 'Market Planning',
        'EI': 'Emotional Intelligence',
        'CO': 'Communications',
        'OP': 'Operations',
        'SM': 'Strategic Management',
        'FI': 'Financial Analysis',
        'EN': 'Entrepreneurship',
        # 'NF': 'Operations Management',
        'EC': 'Economics',
        'Earning Income': "Earning Income",
        'Spending': 'Spending',
        'Saving': 'Saving',
        'Investing': 'Investing',
        'Managing Credit': 'Managing Credit',
        'Managing Risk': 'Managing Risk'
    }

    deca_questions = {
        'PM': [],
        'PD': [],
        'MK': [],
        'PI': [],
        'IM': [],
        'HR': [],
        'CM': [],
        'RM': [],
        'BL': [],
        'CR': [],
        'QM': [],
        'PJ': [],
        'KM': [],
        'PR': [],
        'FM': [],
        'SE': [],
        'MP': [],
        'EI':[],
        'CO': [],

        'SM': [],
        'FI': [],
        'EN': [],
        'OP': [],
        'EC': [],
        'Earning Income': [],
        'Spending': [],
        'Saving': [],
        'Investing': [],
        'Managing Credit': [],
        'Managing Risk': []
    }

    for k, v in deca_codes.items():
        filename = v
        if not os.path.isfile('instruct_area_output/' + v + '.txt'):
            with open('instruct_area_output/' + v + '.txt', mode='x') as f2:
                f2.write("")

    exam_names = {
        'BAC': 'Business Admin Core 2024 Exams',
        'BMA': 'Business Management Administration 2024 Exams',
        'Ent': 'Entrepreneurship 2024 Exams',
        'Fin': 'Finance 2024 Exams',
        'Hospitality': 'Hospitality 2024 Exams',
        'Mktg': 'Marketing 2024 Exams',
        'PF': 'Personal Finance 2024 Exams',
    }

    for filename in os.listdir('output/'):
        examname = exam_names[filename.split(" ")[0]]
        with open('output/' + filename, encoding='utf-8') as f:
            lines = f.readlines()

            num = 1
            question = ""
            key2 = ""
            for i in range(len(lines)):
                if lines[i].startswith(f'{num+1}.'):
                    if not examname in deca_questions[key2]:
                        deca_questions[key2].append(examname)
                        deca_questions[key2].append('\n\n')
                    deca_questions[key2].append(question)
                    key2 = ''
                    question = ''
                    num += 1
                question += lines[i]
                if lines[i].startswith('SOURCE:') and key2 == '':
                    if filename.startswith('PF'):
                        sub = lines[i][8:]
                        key2 = sub[:sub.index(' Grade')]
                    elif ':' in lines[i][8:]:
                        sub = lines[i][8:]
                        key2 = sub[:2] 
                        if key2 == "NF":
                            key2 = 'IM'    
                
                
    for k, v in deca_codes.items():
        filename = v
        with open('instruct_area_output/' + v + '.txt', mode='a', encoding='utf-8') as f3:
            for s in deca_questions[k]:
                f3.write(s)


def count_unique_clusters():
    clusters = set()
    for filename in os.listdir('output/'):
        # if filename == 'PF Area.txt':
        #     continue
       
        with open('output/' + filename, encoding='utf-8') as f:
            lines = f.readlines()
            sources = [lines[i] for i in range(len(lines)) if lines[i].startswith('SOURCE:') and ':' in lines[i][8:]]
            for line in sources:
                line2 = line[8:]
                if line2[2] == ':':
                    clusters.add(line2[:2])
    print(clusters)



def exclude_file(filename):
    return filename == 'PF Area.txt' or filename == 'BMA State.txt' or filename == 'Fin State.txt'

def is_all_uppercase(s):
    # Filter out the non-alphabetical characters
    alphabet_chars = [char for char in s if char.isalpha()]
    
    # Return True if all the remaining characters are uppercase
    return all(char.isupper() for char in alphabet_chars)

def capitalize_tokens(s):
    # Split the string by spaces to get tokens
    tokens = s.split()

    # Capitalize the first letter of each token and lowercase the rest
    capitalized_tokens = [token[0].upper() + token[1:].lower() if len(token) > 1 else token.upper() for token in tokens]

    # Join the tokens back into a single string
    return ' '.join(capitalized_tokens)

def rename_pdfs():
    folder = 'pdfs/'
    for filename in os.listdir(folder):
        try:
            idx = filename.split("_").index("DECA")
        except:
            continue
        print(filename)
            

        new_filename = filename.split("_")[filename.split("_").index("DECA")+1] + " - "

        name = ""
        count = 0
        foundFirstUpper = False
        with pdfplumber.open(folder + filename) as pdf:
            second_page = pdf.pages[1]
            words = second_page.extract_words()
            for word in words[8:]:
                if is_all_uppercase(word['text']):
                    foundFirstUpper = True
                    name += word['text'] + " "
                else:
                    if foundFirstUpper:
                        break
        name = name[0:len(name)-1]
        name = name.replace(",", "")
        name = capitalize_tokens(name)
        new_filename += name
        new_filename += ".pdf"
        old_file = os.path.join(folder, filename)
        new_file = os.path.join(folder, new_filename)
        os.rename(old_file, new_file)


def main():
    # for filename in os.listdir('output/'):
    #     if exclude_file(filename):
    #         continue
    #     with open('output/' + filename, mode='w') as f:
    #         f.write('')
    # for filename in os.listdir('instruct_area_output/'):
    #     with open('instruct_area_output/' + filename, mode='w') as f:
    #         f.write('')
    
    # # organize_q_a()
   
    # # remove_blank_lines()
    # organize_instruct_areas()
    # count_unique_clusters()
    rename_pdfs()
    pass


if __name__ == "__main__":
    main()