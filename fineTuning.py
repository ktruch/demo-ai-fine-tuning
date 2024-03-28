
from openai import OpenAI
import documentsService
from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.environ['OPENAI_API_KEY']
organization_id = os.environ['ORGANIZATION_ID_OPENAI']
client = OpenAI()
model_name = os.environ['MODEL_NAME']
pre_trained_model = client.models.retrieve(model=model_name)
print(pre_trained_model)
print(pre_trained_model.id)

def create_training_data_from_text(text, suffix):
    print("Inside creating data: " + suffix)
    system_content = "You are chatbot of TBSCG company, you are helpful and professional, answer the question precisely, give instructions from points, basing on following text: " + text + "" 
    sample_questions = []
    response = client.chat.completions.create(
        model=model_name,
        n=10,
        messages=[
        {"role": "system", "content": "You are assistant creating a question"},
        {"role": "user", "content": "Create question basing on text: " + text + ""}
     ])
    if response:
        for qa_by_bot in response.choices:
            qa = qa_by_bot.message.content
            sample_questions.append(qa)

    answers = []
    if sample_questions:
        for qa in sample_questions:
            response = client.chat.completions.create(
                    model=model_name,
                    n=10,
                    messages=[
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": qa}])
            answers.append(response.choices[0].message.content)
    input = []
    for i in range(len(sample_questions)):
        record = {"messages": 
                  [
                    {"role": "system", "content": "" + system_content + "" },
                    {"role": "user", "content": "" + sample_questions[i] + ""},
                    {"role": "assistant", "content": "" + answers[i] + ""}
                     ]}
        input.append(record)
        file_name = 'auto-gen-training-data_' + suffix + '.jsonl'
    count = 0
    with open(file_name, 'w') as file:
        for line in input:
            
            line = str(line)
            new_line = line.replace("\\","")
            if count < (len(input)-1):
                file.write(new_line + '\n ')
                count += 1
            else:
                file.write(new_line)
        file.close()
    with open(file_name, 'r') as file:
        lines = file.readlines()
    with open(file_name, 'w') as file:
        for line in lines:
            new_line = line.replace('"',"").replace("'}",'"}').replace("{'messages'",'{"messages"').replace("'role': 'system', 'content': '",'"role": "system", "content": "').replace("'role': 'user', 'content': '",'"role": "user", "content": "').replace("'role': 'assistant', 'content': '",'"role": "assistant", "content": "')
            new_line = new_line.replace("'role': 'system', 'content': ",'"role": "system", "content":"').replace("'role': 'user', 'content':",'"role": "user", "content": "').replace("'role': 'assistant', 'content':",'"role": "assistant", "content": "').replace(".}",'."}').replace("?}",'"}').replace(". }",'."}').replace("? }",'?"}').replace(")}", ')"}')
            new_line = new_line.replace("a}", 'a"}').replace("b}", 'b"}').replace("c}", 'c"}').replace("d}", 'd"}').replace("e}", 'e"}').replace("f}", 'f"}').replace("g}", 'g"}').replace("h}", 'h"}').replace("i}", 'i"}').replace("j}", 'j"}').replace("k}", 'k"}').replace("l}", 'l"}').replace("m}", 'm"}').replace("n}", 'n"}').replace("o}", 'o"}').replace("p}", 'p"}').replace("r}", 'r"}').replace("s}", 's"}').replace("t}", 't"}').replace("u}", 'u"}').replace("v}", 'v"}').replace("w}", 'w"}').replace("x}", 'x"}').replace("y}", 'y"}').replace("z}", 'z"}')
            new_line = new_line.replace("1}", '1"}').replace("2}", '2"}').replace("3}", '3"}').replace("4}", '4"}').replace("5}", '5"}').replace("6}", '6"}').replace("7}", '7"}').replace("8}", '8"}').replace("9}", '9"}').replace("0}", '0"}').replace(">}", '>"}').replace("*}", '*"}').replace("%}", '%"}').replace("$}", '$"}').replace("@}", '@"}')
            new_line = new_line.replace("} {", '}, {').replace("}{", '}, {').replace("  }", ' "}').replace("   }", ' "}').replace("    }", ' "}').replace('" }', '"}').replace('"  }', '"}').replace('"   }', '"}').replace(' }', '"}')
            file.write(new_line)
        file.close()

    finetune(file_name)
    return file

def finetuning_for_all_documents():
    titles_list = documentsService.getListOfDocumentsOnS3()
    filtered_list = [title for title in titles_list if ".pdf" in title]
    print(filtered_list)
    for file_key in filtered_list:
        text = documentsService.getPdfFileTextFromS3(file_key)
        suffix:str = file_key
        suffix: str = suffix.replace("/", "-").replace("\\", "-")
        create_training_data_from_text(text, suffix)
        file_name = file_key.split('/')[-1]
        if os.path.exists(file_name):
            os.remove(file_name)

def finetune(file_name):
    file = client.files.create(
        file=open(file_name, "rb"),
        purpose="fine-tune"
        )

    client.fine_tuning.jobs.create(
        training_file = file.id, 
        model=pre_trained_model.id
        )
