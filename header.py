def header_html(nome=""):
    header = f"""<div class="fixed">
            <div class="menu">
                <div class="logo">
                    <img src="https://github.com/deveucatur/UMADSEDE/blob/main/logo.png?raw=true" alt="Logo do 9Box">
                </div>
                <div class="nome"><p>{nome}</p></div>
            </div>
        </div>"""
    return header

def header_css():
    style = f""".fixed{{
            position: fixed;
            top: 0;
            z-index: 999990;
            left: 50px;
            right: 50px;
        }}

        .menu{{
            display: flex;
            position: absolute;
            align-items: center;
            /*background: linear-gradient(to bottom, #06405c);*/
            background-color: #06405c;
            color: #fff;
            padding: 10px 20px;
            width: 100%;
            height: 46px;
            border-bottom-left-radius: 15px;
            border-bottom-right-radius: 15px;
        }}

        .logo,
        .botoes{{
            margin-right: auto;
        }}

        .logo img{{
            width: 100px;
            font-family: 'M PLUS Rounded 1c', sans-serif;
            font-size: 10px;
            margin: 0;
        }}

        .botoes{{
            margin-top: 10px;
        }}

        .botoes p{{
            font-weight: bold;
            background-color: #ffc000;
            padding: 0px 15px;
            border-radius: 8px;
            font-size: 18px;
            color: #06405c;
        }}

        .botoes button{{
            margin-right: 10px;
            padding: 0px 10px;
            border: none;
            background-color: transparent;
            color: #fff;
            cursor: pointer;
            font-weight: bold;
            font-size: 16px;
            transition: border-color 0.5s ease;
        }}

        .nome p{{
            margin-right: 10px;
            color: #ffc000;
            font-weight: bold;
            font-size: 16px;
            margin-top: 12px;
        }}

        .icone img{{
            width: 35px;
            height: 35px;
        }}

        .icone button{{
            background-color: #9fdafc;
            border-radius: 50%;
            cursor: pointer;
            border: none;
            width: 40px;
            height: 40px;
        }}

        .modulo{{
            display: none;
            position: absolute;
            top: auto;
            right: 0;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            background-color: #9fdafc;
            height: auto;
            width: 175px;
            border-radius: 10px;
            padding: 10px;
            margin-top: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
        }}

        .modulo button{{
            border-radius: 8px;
        }}

        .modulo:after{{
            content: "";
            width: 0;
            height: 0;
            position: absolute;
            border-left: 15px solid transparent;
            border-right: 15px solid transparent;
            border-bottom: 20px solid #9fdafc;
            top: -15px;
            right: 25px
        }}

        .icone:hover .modulo{{
            display: block;
        }}

        .modulo button{{
            display: block;
            width: 100%;
            padding: 5px;
            text-align: left;
            background-color: transparent;
            border: none;
            cursor: pointer;
            font-weight: bold;
            color: #000;
            margin-bottom: 5px;
        }}

        .botoes button:hover{{
            border: none;
            border-bottom: 2px solid #26eda2;
            cursor: pointer;
        }}

        .modulo button:hover{{
            background-color: #91c1dd;
        }}

        .logo:hover{{
            text-decoration: underline;
        }}
        
        @media (max-width: 480px) {{
            .botoes {{
                width: 60%;
                text-align: center;
            }}

            .nome {{
                display: none;
            }}
        }}"""
    return style

