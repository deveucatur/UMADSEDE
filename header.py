def header_html(page_name):
    header = f"""
    <div class="fixed-header">
        <div class="header">
            <div class="logo">
                <img src="https://raw.githubusercontent.com/RahyanRamos/LogoNineBox/main/logo.png" alt="Logo">
            </div>
            <div class="page-name">
                <p>{page_name}</p>
            </div>
        </div>
    </div>
    """
    return header

def header_css():
    style = """
    .fixed-header {
        position: fixed;
        top: 0;
        z-index: 9999;
        left: 0;
        right: 0;
    }

    .header {
        display: flex;
        align-items: center;
        background-color: #FF7F00;  /* Laranja */
        color: #fff;
        padding: 10px 20px;
        width: 100%;
        height: 60px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }

    .logo img {
        height: 40px;
    }

    .page-name {
        margin-left: 20px;
        font-size: 24px;
        font-weight: bold;
    }

    .page-name p {
        margin: 0;
        color: #fff;
    }

    /* Responsividade */
    @media (max-width: 480px) {
        .header {
            flex-direction: column;
            height: auto;
            padding: 10px;
        }
        .page-name {
            margin-left: 0;
            margin-top: 10px;
            text-align: center;
        }
    }
    """
    return style
