import label_studio as ls

client = ls.Client('http://localhost:8080', 'Your API Key secret')
label_config = client.create_config('text_classification', ['Positive', 'Negative', 'Neutral'])
project = client.create_project(title='My Project', label_config=label_config)

project.import_tasks_from_list([
    'Good case, Excellent value.'
    'Needless to say, I wasted my money.',
    'And the sound quality is great.'
    'I advise EVERYONE DO NOT BE FOOLED!'
])
project.annotate()
print(project.get_results(normalize=True))
