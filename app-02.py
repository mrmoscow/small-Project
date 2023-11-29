import dash
from dash import Dash, html, dcc, callback, Input, Output,State
from dash.exceptions import PreventUpdate
import os
import openai

#author: 顏聖峰mrmoscow
#Email: mrmoscow@gmail.com
#since: 2023-07-02
#requistite:
    # 1. dash,  pip install dash
    # 2. openai pip install openai
#input, after runnin  the code. open Browser and link to http://0.0.0.0:8053/
    # 1. 一段英文文章 
#output, 
    #1, 一段中文摘要

openai.api_key = os.getenv("OPENAI_KEY_AIGO23")

def Eng2Chi(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        #engine="gpt-3.5-turbo",
        #prompt=f"Translate English into 繁體中文: {text}",
        prompt=f"請給我下面文章的繁體中文摘要: {text}",
        #prompt = f"Summarize the following English article into traditional Chinese:\n\n{text}",
        temperature=0.8,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    translation = response.choices[0].text.strip()
    return(translation)


app = Dash(__name__,title='英文文摘中文摘要網')

app.layout = html.Div([
    html.H1('OpenAI 作業-英文文稿-中文結論轉換頁面'),
    dcc.Textarea(
        id='textarea-input',
        value='請清除此行，並在這邊輸入英文文章,輸入完畢請按submit\n',
        style={'width': '45%', 'height': 300, 'margin-left':'3%',},
    ),
    html.Div(
        id='textarea-output',
        style={'whiteSpace': 'pre-line','width': '45%', 'height': 300,
               'float':'right', 'border-style':'solid','margin-right':'3%',},
    ),
    #dcc.Textarea(
    #    id='textarea-output2',
    #    value='稍後會顯示中文摘要\n',
    #    style={'width': '45%', 'height': 300, 'float':'right'},
    #),
    html.H6('--貼上文章後，請按下下面轉換'),
    html.Button('轉換', id='textarea-button', n_clicks=0),
    html.H2(''),
    #html.H2('-----App 2, upload MP3 and generation the text -------'),
    #dcc.Upload(html.Button('Upload File'),id='upload-data',),
])

@callback(
    Output('textarea-output', 'children'),
    Input('textarea-button', 'n_clicks'),
    State('textarea-input', 'value')
)
def update_output(n_clicks, value):
    if n_clicks > 0:
        print("Original text:\n",value)
        print("Start The AI transfrom")
        a=Eng2Chi(value)
        print("After transform \n",a)
        return '中文摘要是: \n{}'.format(a)


if __name__ == '__main__':
    app.run_server(debug=True,host='0.0.0.0', port='8053')
