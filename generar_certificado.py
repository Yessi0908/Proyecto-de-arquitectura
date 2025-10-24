#!/usr/bin/env python3
"""
Script para generar certificados SSL auto-firmados para el servidor
"""

from OpenSSL import crypto
import os

def generar_certificado_ssl():
    """Generar certificado SSL auto-firmado"""
    
    # Crear par de llaves
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 2048)
    
    # Crear certificado
    cert = crypto.X509()
    cert.get_subject().C = "ES"
    cert.get_subject().ST = "Madrid"
    cert.get_subject().L = "Madrid"
    cert.get_subject().O = "Sistema Invernadero"
    cert.get_subject().OU = "Desarrollo"
    cert.get_subject().CN = "localhost"
    
    # Agregar extensiones para navegadores modernos
    cert.add_extensions([
        crypto.X509Extension(b"subjectAltName", False, b"DNS:localhost,DNS:127.0.0.1,DNS:192.168.1.7,IP:127.0.0.1,IP:192.168.1.7"),
        crypto.X509Extension(b"keyUsage", True, b"digitalSignature,keyEncipherment"),
        crypto.X509Extension(b"extendedKeyUsage", True, b"serverAuth"),
    ])
    
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(365*24*60*60)  # Válido por 1 año
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(key)
    cert.sign(key, 'sha256')
    
    # Guardar archivos
    with open("server.crt", "wb") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        
    with open("server.key", "wb") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
        
    print("✅ Certificados SSL generados:")
    print("   📄 server.crt (certificado)")
    print("   🔑 server.key (llave privada)")
    print()
    print("🔧 Para usar HTTPS:")
    print("   1. El navegador mostrará una advertencia de seguridad")
    print("   2. Haz clic en 'Avanzado' y luego en 'Continuar a localhost'")
    print("   3. El sitio será seguro con HTTPS")

if __name__ == "__main__":
    generar_certificado_ssl()