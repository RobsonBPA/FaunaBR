# Fauna BR - Os Animais Brasileiros
## Fauna BR - Brazilian Animals

## Descrição
O FaunaBR é um jogo desenvolvido em Python com a biblioteca Pygame, como parte do Trabalho de Conclusão de Curso (TCC) do Ensino Médio integrado ao Técnico em Desenvolvimento de Sistemas.

O projeto tem como principal objetivo promover a conscientização sobre a fauna brasileira, incentivando o conhecimento e a valorização da biodiversidade do Brasil por meio de uma experiência interativa e divertida.

Desenvolvido por uma equipe de estudantes, o jogo reúne programação, design, sonorização e roteiro para transformar o aprendizado sobre os animais brasileiros em uma experiência envolvente.

## Description
FaunaBR is a game developed in Python using the Pygame library, created as a final project for a high school program integrated with a technical course in Systems Development.

The project’s primary objective is to raise awareness about Brazilian fauna, encouraging a better understanding and appreciation of Brazil’s biodiversity through an interactive and entertaining experience.

Developed by a team of students, the game combines programming, design, sound, and storytelling to turn learning about Brazilian animals into an engaging experience.



## Integrantes
Angelo Gabriel de Jesus Santos - *Designer e Engenheiro de Som*
Henrique Ferreira de Souza - *Designer*
Robson Bassanezi Pasetto Aparecido - *Desenvolvedor Full Stack, Designer e Gerente de Projeto*
Rodolfo Ribeiro da Silva - *Roteirista*

## Members
Angelo Gabriel de Jesus Santos - *Designer and Sound Engineer*
Henrique Ferreira de Souza - *Designer*
Robson Bassanezi Pasetto Aparecido - *Full Stack Developer, Designer and Project Manager*
Rodolfo Ribeiro da Silva - *Game Writer*



## Objetivo
Este projeto TCC (Trabalho de Conclusão de Curso) desenvolvido em Python com a biblioteca Pygame tem como objetivo ser um jogo para conscientizar as pessoas sobre os animais do Brasil.

## Objectives
This undergraduate thesis project, developed in Python using the Pygame library, aims to be a game to raise awareness about Brazilian animals.

## Executar o jogo

Requisitos: Python 3.10 ou superior, Pygame CE 2.x e PyTMX 3.x.

```powershell
py -m pip install -r requirements.txt
py main.py
```

O jogo deve ser iniciado a partir da pasta do projeto. Os recursos são localizados
em relação ao próprio projeto no modo de desenvolvimento e a partir da pasta
temporária do PyInstaller no executável.

## Gerar executável para Windows

Instale o PyInstaller e empacote o jogo com os recursos:

```powershell
py -m pip install pyinstaller
py -m PyInstaller --noconfirm --onefile --windowed --name FaunaBR --add-data "assets;assets" --hidden-import pytmx.util_pygame main.py
```

O executável será criado em `dist/FaunaBR.exe`.


## Imagens do Projeto / Project Images

### 02/06/2026
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/a749dcb7-b80e-4e69-8f7b-ed974af362df"/>

### 22/06/2026
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/cf269d70-7cbf-47fa-902f-1dc3d60a93b5"/>

### 28/07/2026
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/3bfe9096-c577-4d1d-82cf-141148d0f843"/>

### 27/10/2026
<img width="1918" height="1078" alt="unnamed" src="https://github.com/user-attachments/assets/42bde9cf-d552-4cb4-a2a9-47f5062538c2"/>