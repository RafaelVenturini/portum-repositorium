# Avaliação do Projeto Final

## Sobre a Avaliação

A apresentação do projeto valerá **10,0 pontos**, distribuídos da seguinte forma:

| Componente | Pontuação |
|------------|------------|
| Presença e participação ativa durante a apresentação | 3,0 pontos |
| Critérios técnicos | 7,0 pontos |
| **Total** | **10,0 pontos** |

Os critérios técnicos foram elaborados para permitir a avaliação de projetos desenvolvidos em diferentes tecnologias, como Flask, FastAPI, Django, Node.js, entre outras.

O objetivo principal é avaliar a aplicação dos conceitos trabalhados ao longo da disciplina, incluindo:

- Arquitetura modular;
- Organização e qualidade de código;
- Validação de dados;
- Persistência de informações;
- Testes automatizados;
- Boas práticas de desenvolvimento.

Projetos desenvolvidos em Flask poderão aproveitar diretamente diversos conteúdos vistos em aula, porém soluções implementadas em outras tecnologias serão avaliadas de forma equivalente, desde que demonstrem os mesmos conceitos.

---

# Critérios Técnicos (7,0 pontos)

| Critério | O que será avaliado | Pontuação |
|-----------|--------------------|------------|
| **1. Arquitetura Modular e Fábrica de Aplicação** | Uso de padrão equivalente ao *Application Factory* (Flask) ou estrutura similar bem organizada, como `create_app()`, App Factory, Dependency Injection ou módulo central de inicialização. | **1,0 ponto** |
| **2. Organização em Módulos, Blueprints ou Rotas** | Separação adequada de responsabilidades através de módulos independentes. Exemplos: Blueprints (Flask), APIRouter (FastAPI), Apps (Django), módulos de rotas (Node.js), entre outros. | **1,0 ponto** |
| **3. Formulários e Validação** | Implementação de validação no servidor, utilizando ferramentas adequadas à tecnologia escolhida. Exemplos: Flask-WTF, WTForms, Pydantic, Django Forms, validações de API, entre outros. | **1,0 ponto** |
| **4. Interface e Frontend** | Utilização adequada de templates ou frontend estruturado, com preocupação estética, usabilidade e responsividade. Exemplos: Jinja2, React, Vue, HTMX, Bootstrap, Bulma, Tailwind CSS, etc. | **1,0 ponto** |
| **5. Testes Automatizados** | Existência de testes automatizados para funcionalidades relevantes do sistema. Exemplos: pytest, unittest, Jest, Flask-Testing e similares. | **1,0 ponto** |
| **6. Persistência de Dados e ORM** | Utilização adequada de banco de dados, ORM ou mecanismo equivalente, incluindo modelagem coerente das entidades e relacionamentos. | **1,0 ponto** |
| **7. Qualidade de Código e Boas Práticas** | Organização do projeto, uso de variáveis de ambiente, tratamento de erros, logging, separação de responsabilidades, legibilidade do código e boas práticas de versionamento. | **1,0 ponto** |

---

# Entrega Obrigatória do Projeto (Auditoria Técnica)

A entrega completa do projeto será utilizada como processo formal de auditoria e validação dos critérios técnicos apresentados anteriormente.

Dessa forma, a pontuação dos **7,0 pontos técnicos** será baseada tanto na apresentação quanto na análise detalhada dos arquivos entregues.

## Material a ser Entregue

### 1. Código-fonte do Projeto

- Compactar todos os arquivos do projeto em um único arquivo `.zip`;
- Não incluir pastas de ambiente virtual (`venv`, `.venv`) nem diretórios de cache (`__pycache__`);
- Nomear o arquivo seguindo o padrão:

```text
GrupoX_NomeDoProduto.zip
```

### 2. Documentação Técnica (Obrigatoriamente em PDF)

O documento deverá conter, no mínimo:

1. Título do projeto;
2. Nome dos integrantes do grupo;
3. Descrição geral do produto e suas funcionalidades;
4. Diagrama do banco de dados (Modelo Entidade-Relacionamento ou equivalente);
5. Detalhamento técnico das principais partes do código, com exemplos relevantes;
6. Explicação da arquitetura adotada;
7. Tecnologias utilizadas;
8. Justificativa da escolha tecnológica (caso não tenha sido utilizado Flask);
9. Passo a passo para execução do projeto;
10. Principais desafios encontrados e respectivas soluções adotadas.

---

# Observações Importantes

> Projetos entregues sem a documentação em PDF ou com código-fonte incompleto terão seus critérios técnicos avaliados prioritariamente com base na apresentação realizada em sala, o que poderá comprometer significativamente a nota final.

> Recomenda-se que todos os integrantes estejam preparados para explicar as decisões técnicas adotadas durante o desenvolvimento do projeto.