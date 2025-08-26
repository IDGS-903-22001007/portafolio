from flask import Flask, render_template, request, flash, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import ssl

app = Flask(__name__)
app.secret_key = 'mi_clave_secreta_super_segura_2024' 

EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'email': 'brayan.saul67@gmail.com',
    'password': 'qand byxs aehe zfui'  # Con espacios como te lo dio Google
}

def send_email(name, email, message):
    """Función para enviar email con mejor manejo de errores"""
    try:
        print(f"=== INICIANDO ENVÍO DE EMAIL ===")
        print(f"Desde: {EMAIL_CONFIG['email']}")
        print(f"Servidor: {EMAIL_CONFIG['smtp_server']}:{EMAIL_CONFIG['smtp_port']}")
        
        # Crear mensaje
        msg = MIMEMultipart('alternative')
        msg['From'] = EMAIL_CONFIG['email']
        msg['To'] = EMAIL_CONFIG['email']
        msg['Reply-To'] = email
        msg['Subject'] = f'🔔 Contacto Portafolio - {name}'
        
        # Cuerpo del mensaje
        body = f"""
🌟 NUEVO MENSAJE DESDE TU PORTAFOLIO WEB 🌟

👤 Nombre: {name}
📧 Email: {email}
📅 Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

💬 Mensaje:
{message}

---
📱 Para responder, simplemente responde a este email.
🌐 Enviado desde: bryan-portafolio.com
        """
        
        # Adjuntar texto
        text_part = MIMEText(body, 'plain', 'utf-8')
        msg.attach(text_part)
        
        print("✅ Mensaje creado correctamente")
        
        # Conectar al servidor con SSL
        print("🔌 Conectando al servidor SMTP...")
        context = ssl.create_default_context()
        
        with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
            print("🔐 Iniciando TLS...")
            server.starttls(context=context)
            
            print("🔑 Iniciando sesión...")
            server.login(EMAIL_CONFIG['email'], EMAIL_CONFIG['password'])
            
            print("📤 Enviando mensaje...")
            server.send_message(msg)
            
        print("✅ ¡Email enviado exitosamente!")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Error de autenticación: {e}")
        print("🔧 Verifica tu contraseña de aplicación de Gmail")
        print("📋 Pasos:")
        print("   1. Ve a https://myaccount.google.com/apppasswords")
        print("   2. Genera una nueva contraseña de aplicación")
        print("   3. Reemplázala en el código")
        return False
        
    except smtplib.SMTPConnectError as e:
        print(f"❌ Error de conexión: {e}")
        print("🔧 Verifica tu conexión a internet")
        return False
        
    except smtplib.SMTPException as e:
        print(f"❌ Error SMTP: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        print(f"❌ Tipo de error: {type(e)}")
        return False

def save_message_to_file(name, email, message):
    """Guardar mensaje en archivo local"""
    try:
        with open('mensajes_contacto.txt', 'a', encoding='utf-8') as f:
            f.write(f"""
=== NUEVO MENSAJE ===
Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Nombre: {name}
Email: {email}
Mensaje: {message}
{'='*50}

""")
        print("Mensaje guardado en archivo local")
        return True
    except Exception as e:
        print(f"Error al guardar mensaje: {e}")
        return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    projects_data = [
        {
            'title': 'EcoSport Frontend - Angular',
            'description': 'Frontend de aplicación web para tienda deportiva desarrollado con Angular y TypeScript. Interfaz moderna y responsiva con funcionalidades completas de e-commerce, incluyendo catálogo de productos, carrito de compras y gestión de usuarios.',
            'technologies': ['Angular', 'TypeScript', 'HTML5', 'CSS3', 'Bootstrap', 'RxJS'],
            'github_url': 'https://github.com/IDGS-903-22001007/angular-producto-app',
            'features': ['SPA con Angular', 'Diseño responsivo', 'Componentes reutilizables', 'Routing dinámico', 'Integración con API REST']
        },
        {
            'title': 'EcoSport API - Backend C#',
            'description': 'API REST desarrollada en C# .NET para el backend de la tienda deportiva EcoSport. Maneja toda la lógica de negocio, autenticación, gestión de productos y procesamiento de pedidos con arquitectura robusta.',
            'technologies': ['C#', '.NET Core', 'Entity Framework', 'SQL Server', 'API REST', 'JWT'],
            'github_url': 'https://github.com/IDGS-903-22001007/ApiEcoSport',
            'features': ['API RESTful completa', 'Autenticación JWT', 'CRUD de productos', 'Gestión de pedidos', 'Base de datos SQL Server']
        },
        {
            'title': 'App de Riego Automático - Android',
            'description': 'Aplicación móvil desarrollada en Android con Kotlin para controlar un sistema de riego automático. Permite monitorear y gestionar el riego de plantas de forma remota mediante una interfaz intuitiva.',
            'technologies': ['Kotlin', 'Android Studio', 'XML Layouts', 'IoT'],
            'github_url': 'https://github.com/IDGS-903-22001007/AndroidRiego',
            'features': ['Control remoto de riego', 'Monitoreo en tiempo real', 'Programación de horarios', 'Interfaz nativa Android']
        },
        {
            'title': 'API Dragon Ball - Kotlin', 
            'description': 'API REST desarrollada en Kotlin para consultar información de personajes, transformaciones y sagas de Dragon Ball. Proyecto que demuestra conocimientos en desarrollo de APIs y programación en Kotlin.',
            'technologies': ['Kotlin', 'API REST', 'JSON', 'Android'],
            'github_url': 'https://github.com/IDGS-903-22001007/ApiDragonBall',
            'features': ['Endpoints de personajes', 'Consultas de transformaciones', 'Información de sagas', 'Respuestas JSON']
        }
    ]
    return render_template('projects.html', projects=projects_data)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()
        
        print(f"\n=== NUEVO FORMULARIO RECIBIDO ===")
        print(f"Nombre: {name}")
        print(f"Email: {email}")
        print(f"Mensaje: {message[:50]}...")
        
        # Validación mejorada
        if not name or not email or not message:
            print("❌ Formulario incompleto")
            flash('Por favor, completa todos los campos.', 'error')
            return render_template('contact.html')
        
        if '@' not in email or '.' not in email.split('@')[-1]:
            print("❌ Email inválido")
            flash('Por favor, ingresa un email válido.', 'error')
            return render_template('contact.html')
        
        print("✅ Validación pasada, intentando enviar...")
        
        # Intentar enviar email
        email_sent = send_email(name, email, message)
        
        if email_sent:
            print("✅ Email enviado correctamente")
            flash('¡Mensaje enviado correctamente! Te responderé pronto.', 'success')
        else:
            print("❌ Email falló, guardando en archivo...")
            if save_message_to_file(name, email, message):
                flash('¡Mensaje recibido y guardado! Te contactaré pronto.', 'success')
            else:
                flash('Hubo un error. Por favor, intenta contactarme directamente.', 'error')
        
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

