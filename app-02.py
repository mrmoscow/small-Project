#from dash import Dash, html, dcc
import dash
from dash import Dash, html, dcc, callback, Input, Output,State
from dash.exceptions import PreventUpdate
import os
import openai

#author: 顏聖峰
#適用dash 語言，開啟本地端web 應用

openai.api_key = os.getenv("OPENAI_KEY_AIGO23")

def Eng2Chi(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        #engine="gpt-4",
        #prompt=f"Translate English into 繁體中文: {text}",
        prompt=f"請給我繁體中文摘要: {text}",
        #prompt = f"Summarize the following English article into Chinese:\n\n{text}"
        temperature=0.5,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    translation = response.choices[0].text.strip()
    return(translation)


app = Dash(__name__,title='英文文摘中文摘要網')

app.layout = html.Div([
    html.H1('OpenAI 作業-英文文稿-中文結論轉換頁面'),
    #html.Div(children='Hello World')
    dcc.Textarea(
        id='textarea-input',
        value='請清除此行，並在這邊輸入英文文章\n',
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
    html.H3('------------'),
    html.Button('Submit', id='textarea-button', n_clicks=0),
])

@callback(
    Output('textarea-output', 'children'),
    Input('textarea-button', 'n_clicks'),
    State('textarea-input', 'value')
)
def update_output(n_clicks, value):
    if n_clicks > 0:
        print("Start The AI transfrom")
        a=Eng2Chi(value)
        print(a)
        #return 'You have entered: \n{}\t{}'.format(value,a)
        return '中文摘要是: \n{}'.format(a)

'''
@callback(
    Output('textarea-example-output', 'children'),
    Input('textarea-example', 'value'))
def update_output(value):
    return 'You have entered: \n{}'.format(value)
'''

if __name__ == '__main__':
    app.run_server(debug=True,host='0.0.0.0', port='8053')
