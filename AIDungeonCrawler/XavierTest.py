from openai import OpenAI
import textwrap
client = OpenAI(
    api_key = "sk-proj-MfQUU6kDUqNSxpmi7q9ET3BlbkFJbM27VwUuRHqM4qi2ePKh"

)
def enemygen(lol):


    system_data = [
        {"role": "system", "content": "Generate a generic dungeon crawler enemy, create a name. Then give a brief description. Then specify if the armor is Light, Medium, or Heavy after that using that wording Then say if its Quick, Average, or Slow, with that wording. "},
        {"role": "user", "content": lol}
    ]

    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = system_data
    )

    assistant_response = response.choices[0].message.content
    system_data.append({"role": "assistant", "content": assistant_response})
    print('\n'.join(textwrap.wrap(assistant_response, 75)))
    return assistant_response
l = str(enemygen(""))
k = l.find("Description: ")
c = 0
name = ''
for i in range(6,k):
    name = name + l[i]
print(name)

match l[len(l)-1]:
    case "k":
        print("Quick")
        c = 5
    case'e':
        print("Average")
        c = 7
    case 'w':
        print("Slow")
        c = 4

match l[len(l)-1-c-9]:

    case 'y':
        print("Heavy")
        c += 5
    case 'm':
        print("Medium")
        c = c + 6
    case 't':
        print("Light")
        c = c + 5

description = ''
for i in range(k, (len(l)-c-17)):
    description = description + l[i]

print (description)
