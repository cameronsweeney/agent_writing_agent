import json

from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

def create_agent(agent_description):
  response = client.chat.completions.create(
    messages=[
      {
      "role": "system",
      "content": "You are an expert agent-writing agent. You'll be creating an agent by filling out the system prompt. Please include instructions for how to perform the task that is asked of you and return only JSON that is structured like this example:\n```json\n{\n      \"role\": \"system\",\n      \"content\": \"You are an expert AGENT_ROLE agent. Please return a well-described agent that has clear criteria for success. \"\n    },\n    {\n      \"role\": \"user\",\n      \"content\": \"Context for the request goes here.\"\n    }\n}\n```\nThe user will provide a request, your role is to write the JSON (and only the JSON) that will make the request occur. Write the instructions in the second person, as if you are giving instructions to a person. Do not instruct the agent to create an agent."
      },
      {
         "role": "user",
         "content": agent_description
      }
    ],
    model="gpt-4-1106-preview",
    temperature=1,
    max_tokens=1024,
    response_format={ "type": "json_object" },
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )
  return response.choices[0].message.content

def agent_config_builder(agent_description):
  agent_config_string = create_agent(agent_description)
  parsed_agent = False
  while not parsed_agent:
    try:
      agent_configuration = json.loads(agent_config_string)
      parsed_agent = True
    except:
      agent_config_string = create_agent(agent_description)
  return agent_configuration

def agent_builder(prompt, agent_configuration, json=False):
  agent_configuration.append({
    "role": "user",
    "content": prompt
  })
  if json:
    response = client.chat.completions.create(
        messages=agent_configuration,
        model="gpt-4-1106-preview",
        temperature=1,
        max_tokens=1024,
        response_format={ "type": "json_object" },
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
      )
  else:
    response = client.chat.completions.create(
      messages=agent_configuration,
      model="gpt-4-1106-preview",
      temperature=1,
      max_tokens=1024,
      # response_format={ "type": "json_object" },
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
  return response.choices[0].message.content

old_agent_description = """
Write only the system prompt for a project management agent whose role is to generate questions.
Based on a brief project description, the agent should output suggestions for guiding purpose and principles to clarify aspects about the project such as scope and motivation. This agent should also write a couple of relevant, insightful questions to determine the guiding purpose and principles of this project.
"""

agent_description = """Please output suggestions for guiding purpose and principles to clarify aspects about the project such as scope and motivation. Please also write a couple of relevant, insightful questions to determine the guiding purpose and principles of this project.
"""

output = create_agent(agent_description)

print(output)

if "```json" in output:
    just_json_output = output.split("```")[1].strip("json\n")
else:
    just_json_output = output

with open("output3.txt", 'w') as file:
    file.write(just_json_output)