# proSenectute_sw_assistant
AI Assisstant for social worker in Pro Senectute for requirements information on a financial help for clients.


Ausgangslage: Ein Angebot der Pro Senectute ist die Individuelle Finanzhilfe. Diese Unterstützung richtet sich an Personen im AHV-Alter, die sich in einer finanziellen Notlage befinden, und wird von der Pro Senectute im Auftrag des Bundes bereitgestellt. Sie bietet Unterstützung bei dringend notwendigen Ausgaben, welche weder durch private Mittel noch durch die Sozialversicherung gedeckt werden können. Die Anträge für Individuelle Finanzhilfe werden von der Pro Senectute geprüft. Diese Anträge werden nicht nach Lust und Laune bewilligt… hierzu gibt es strenge und komplizierte Reglemente, welche eingehalten werden müssen. Diese Reglemente erschweren die Einarbeitung unserer Sozialarbeitenden.

Zielsetzung: Entwickeln einer KI-Gestützten Suchmaschine für die Reglemente der Individuellen Finanzhilfe, welche genaue und zuverlässige Antworten gibt. Die Suchmaschine soll in der Lage sein, eine Quelle der gegebenen Antworten zu geben (z.B. “Dokument” Abschnitt 1, Ziffer 2). Es soll die Möglichkeit geben, diese Suchmaschine einfach auf andere Reglemente zu erweitern (z.B. Internes Personalreglement).

Ressourcen:

Die Reglemente der Individuellen Finanzhilfe.
Fallbeispiel für ein IF-Gesuch
Merkblatt Individuelle Finanzhilfe (Link: https://drive.google.com/drive/folders/1scZKSsrJ7IDLHsuO5f2C-v5_IngycciD?usp=sharing)
Mateo Soppelsa (anwesend)

Requirements that would help to do it well:

- Examples of questions, queries for the AI assistant on the subject that need to look at.
-


Ideas for a solution:

Using a RAG (retrieval augmented generation) AI assisstant that discects the documents and tries to answer the question based on the instructions given. 
A Webpage Solution for the intranet of the organisation would be most optimal.
It should run on a microsoft server in the the data center. 
 Output would be a text answers, perhaps with links, name of the document, page and or citation of the text section containing the refered information.

Open questions:
- Hardware, Software, Solition requirements?
Social Worker has a MS windows 11 OS without GPU to run a LLM solutution on premise.
A browser solution would be bettet.


