def tag_news(title, html_content):
    tags = []

    keywords = {
        "Educação": ["IFES", "UFES", "alunos", "ensino"],
        "Meio Ambiente": ["meio ambiente", "prevenção ambiental"],
        "Impacto Social": ["impacto social", "cidadania", "mulheres", "feminino"],
        "Economia": ["economia", "emprego", "desenvolvimento", "socioeconômico"],
    }

    content = f"{title} {html_content}".lower()

    for tag, words in keywords.items():
        if any(word.lower() in content for word in words):
            tags.append(tag)

    return tags


print(tag_news("Porto Central recebe turma da Ufes para visita técnica às obras", ""))