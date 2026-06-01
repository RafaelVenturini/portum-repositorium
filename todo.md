# Project

## Database

- [x] news_letter
  - [x] user_email
  - [x] register_at
  - [x] cancelled_at
    - [x] active

- [x] articles
  - [x] news_id
  - [x] html
  - [x] date_colleted
  - [x] updated_at
  - [x] url
  - [x] news_before
  - [x] author

-[ ] tags
  -[ ] tag_id
  -[ ] name

-[ ] article_tags



- UTILITYS 
  - [ ] transformar todas as funções genericas de scraper.porto_central em funções reutilizaveis, a fim de reaproveita-las quando for puxar de novos sites
  - [ ] fazer um sistema de tageamento nos artigos
  - [ ] criar a newsletter com base no tageamento (só avisar a pessoa sobre as noticias que ela se inscreveu)

## Scrapping

- [ ] Fonts
  - [x] Central port oficial site
    - [x] <https://www.portocentral.com.br/wp-json/wp/v2/posts>
    - [x] <https://www.portocentral.com.br/wp-json/>
  - [ ] Globo News
  - [ ] A Gazeta
- [ ] key-words
  - [ ] Porto Central
  - [ ] Central Port
  - [ ] Presidente Kennedy

### Things to search

- RSS
  - Aparentemente uma forma permissiva de fazer o scrap, sem dar probleminhas rs
- robots.txt
  - Meu maior inimigo, burlar isso com playwright bem configurado (botar tamanho de tela real, opções comuns de browser essas coisas)

## UI

- [ ] Categorys
  - [ ] population
  - [ ] sustentability
  - [ ] business
  - [ ] opinions
- [ ] About
  - [ ] Explain the UVV project
  - [ ] Explain about the differences of ports in Brazil

## Necessities

- [x] CLI
  - [x] Database
    - [x] Create
    - [x] Populate
    - [x] Destroy
  - [ ] Tests
    - [ ] Direct fetch is working
    - [ ] Beautiful soup is working
    - [ ] Playwright is working

  