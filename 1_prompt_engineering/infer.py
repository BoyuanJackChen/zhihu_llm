import openai
import os
import json
from typing import List
from pydantic import BaseModel

class StepByStepAIResponse(BaseModel):
    title: str
    steps: List[str]

openai.api_key = "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"

schema = StepByStepAIResponse.schema() # returns a dict like JSON schema
# schema content looks like below
"""
{
    'title': 'StepByStepAIResponse',
    'type': 'object',
    'properties': {'title': {'title': 'Title', 'type': 'string'},
    'steps': {'title': 'Steps', 'type': 'array', 'items': {'type': 'string'}}},
    'required': ['title', 'steps']
}
"""


response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
       {"role": "user", "content": "Explain how to assemble a PC"}
    ],
    functions=[
        {
          "name": "get_answer_for_user_query",
          "description": "Get user answer in series of steps",
          "parameters": StepByStepAIResponse.schema()
        }
    ],
    function_call={"name": "get_answer_for_user_query"}
)

output = json.loads(response.choices[0]["message"]["function_call"]["arguments"])
print(output)

# output content
"""
{'title': 'Assembling a PC', 
'steps': 
    [
        "Decide on your PC's purpose: The components you choose will depend on what you will use your PC for. Gaming, office work, media editing and student use all have different requirements.", 
        'Choose your components: Based on your needs, select components like the CPU, RAM, hard drive, graphics card, power supply unit, and cooling system.', 
        "Purchase a suitable case: Make sure it's large enough to fit all of your components and has proper ventilation.", 
        'Prepare your case: Remove the side panels, lay the case flat on your work surface, and organize your tools and components.', 
        'Install the power supply: Secure it to the inside of the case using the screws provided.', 
        "Set up the motherboard outside of the case: Install the CPU, CPU cooler, and RAM according to the manufacturer's instructions.", 
        'Install the motherboard into the case: Make sure you match the screw holes on the motherboard with the standoffs in the case.', 
        'Connect the motherboard to the power supply: Use the 24-pin connector for the main power connection, and the 8-pin connector for CPU power.', 
        'Install the hard drive or SSD: Secure the drive in a 3.5-inch bay (for hard drives) or a 2.5-inch bay (for SSDs), then connect the power and data cables.', 
        'Install the graphics card: Insert it into the appropriate PCI slot on the motherboard, then connect it to the power supply if necessary.', 
        'Connect any additional peripherals: This may include a DVD drive, sound card, etc.', 
        'Install your operating system: Insert the installation disc or bootable flash drive, then follow the on-screen instructions to install.', 
        "Install any necessary drivers: Your components may have come with a disc containing drivers, or you can download them from the manufacturer's website.", 
        'Complete a final check: Ensure all components are securely connected, and that the PC starts up and runs correctly.'
    ]
}
"""