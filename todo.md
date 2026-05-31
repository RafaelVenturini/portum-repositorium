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

## Scrapping

- [ ] Fonts
  - [ ] Central port oficial site
    - [ ] <https://www.portocentral.com.br/wp-json/wp/v2/posts>
    - [ ] <https://www.portocentral.com.br/wp-json/>
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

- [ ] CLI
  - [ ] Database
    - [ ] Create
    - [ ] Populate
    - [ ] Destroy
  - [ ] Tests
    - [ ] Direct fetch is working
    - [ ] Beautiful soup is working
    - [ ] Playwright is working
