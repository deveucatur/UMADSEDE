def header_html(page_name=""):
    header = f"""
    <div class="fixed-header">
        <div class="header">
            <div class="logo">
                <img src="https://github.com/deveucatur/UMADSEDE/blob/main/logo.png?raw=true" alt="Logo">
            </div>
            <div class="nav-menu">
                <a href="/home" target="_self">Home</a>
                <a href="/eventos" target="_self">Eventos</a>
                <a href="/contato" target="_self">Contato</a>
                <!-- Adicione mais links conforme necessário -->
            </div>
            <div class="user-actions">
                <!-- Ícones de redes sociais ou ações do usuário -->
                <!-- Exemplo: <a href="#"><img src="link_do_ícone" alt="Ícone"></a> -->
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
        justify-content: space-between;
        background-color: #FF8C00;  /* Laranja */
        color: #fff;
        padding: 10px 20px;
        width: 100%;
        height: 70px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }

    .logo img {
        height: 50px;
    }

    .nav-menu {
        display: flex;
        gap: 20px;
    }

    .nav-menu a {
        color: #fff;
        text-decoration: none;
        font-size: 18px;
        font-weight: bold;
        transition: color 0.3s;
    }

    .nav-menu a:hover {
        color: #FFD700;  /* Dourado */
    }

    .user-actions {
        display: flex;
        align-items: center;
        gap: 15px;
    }

    .user-actions a img {
        width: 30px;
        height: 30px;
    }

    /* Responsividade */
    @media (max-width: 768px) {
        .header {
            flex-direction: column;
            height: auto;
            padding: 15px;
        }
        .nav-menu {
            flex-direction: column;
            align-items: center;
            margin-top: 10px;
        }
        .nav-menu a {
            font-size: 16px;
        }
    }
    """
    return style
