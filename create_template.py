if __name__ == '__main__':
    with open('template.txt', 'w', encoding='utf-8') as file:
        file.write(
            """
difficulty:basic,category:XXX,subcategory:XXX


question:XXX
options:X,X,X,X
answer:0
explanation:XXX

question:XXX
options:X,X,X,X
answer:0
explanation:XXX


difficulty:advance,category:XXX,subcategory:XXX


question:XXX
options:X,X,X,X
answer:0
explanation:XXX
            """
        )
