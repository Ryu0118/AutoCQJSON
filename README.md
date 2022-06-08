## Usage
Download the source and add the text file in the same directory.<br>
Then run<br>
`$ python main.py question.txt`

Create metadata for questions
``` Question.txt
difficulty:basic,category:数学,subcategory:足し算
```

Add question
```
difficulty:basic,category:数学,subcategory:足し算

question:1+1=
options:1,2,3,4
answer:2
explanation:1+1=2

question:2+1=
options:1,2,3,4
answer:3
explanation:2+1=3

difficulty:basic,category:数学,subcategory:掛け算

question:2*1=
options:1,2,3,4
answer:2
explanation:2*1=2

difficulty:advance,category:歴史,subcategory:世界史
...

```

Result
```Question.json
{
  "basic": [
    {
      "数学": [
        {
          "足し算": [
            {
              "question": "1+1=",
              "options": [
                "1",
                "2",
                "3",
                "4"
              ],
              "answer": 2,
              "explanation": "1+1=2"
            },
            {
              "question": "2+1=",
              "options": [
                "1",
                "2",
                "3",
                "4"
              ],
              "answer": 3,
              "explanation": "2+1=3"
            }
          ]
        },
        {
          "掛け算": [
            {
              "question": "2*1=",
              "options": [
                "1",
                "2",
                "3",
                "4"
              ],
              "answer": 2,
              "explanation": "2*1=2"
            }
          ]
        }
      ]
    }
  ]
}
```
