'''
This file contains the message handlers for the bot.
'''
from config import logger
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

llm=ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Brute force method to handle history
'''
NOTE : as the server will restart the conversation history will be lost.
'''

async def text_message_handler(update, context):
    """Handle regular text messages"""
    user = update.effective_user
    user_message = update.message.text

    logger.info(f"Received message from {user.first_name}: {user_message}")

    try:
        message=[
            (
                'system',
                '''
                You are a helpful assistant that will help the user to get started with ai and become master in ai.
                If someone asks about resorces refer this
                ## Resource Information:
                1. Free Course on AI Engineering <https://www.youtube.com/playlist?list=PLSdiMs6f-QAc8Iq1kKJMP8kSYAEUONLgE>
                *Covers Github, CI, Chat GPT Clone, Prompt Engineering, and Document Search*

                2. Sample Resume Format <https://drive.google.com/drive/folders/1cjVgS-Gd-_Cgdvo6AIlnNmqu5Kg5xffX>
                *Contains resumes to help crack data-related jobs easily*

                3. Python Practice Sheet <https://docs.google.com/document/d/12dFCPtp9yPhwN-vXl2VyHPf5hz3IpmMzjYCE0YKXsLY/edit>
                *Strengthens Python skills for data roles*

                4. AI/ML Books <https://drive.google.com/drive/folders/1c2afEqY613bJvbU3cmzyhJwclCRBsDQ5>
                *In-depth knowledge resources for Data Science and AI*

                5. Unique Data Science Project Ideas <https://www.linkedin.com/in/adityaabhatt/details/projects/>
                *Unique Data Science projects in healthcare, education, and economics*

                6. Important Certifications for Data Science <https://www.linkedin.com/in/adityaabhatt/details/certifications/>
                *Certifications completed by the founder*

                7. Free Cheat Sheets for Python, R, ML, and Data Science <https://drive.google.com/drive/folders/1AqljqYrrns_zdhpTZlukwRx6-N-L5VcN>
                *Helpful for interview preparation and quick revision*

                8. Free Interview 30 Day Guide <https://drive.google.com/file/d/1LMLy71UnVeItScyMHJe1GmxOCtsPXANk/view>
                *Covers almost all interview questions*

                9. End-to-End Data Analyst Project Idea <https://www.youtube.com/watch?v=E41JQb8qNEI>
                *Project involving Python, Gen AI, SQL, and Power BI for Food Industry use case*

                10. Data Science Project Ideas <https://www.youtube.com/watch?v=E41JQb8qNEI>
                    *Unique Data Science projects in healthcare, education, economics, product development, and Generative-AI*

                11. Latest Blogs on Artificial Intelligence <https://aiwithaditya.odoo.com/blog>
                    *Founder's blogs on AI topics*

                12. AI and BI Solution for Human Resources <https://aiwithaditya.odoo.com/blog/hr-management-using-bi-gen-ai-3>
                    *Founder's blog on integrating AI in HR*

                13. Latest AI Research <https://arxiv.org/list/cs.AI/recent>
                    *Access to recent AI research papers on arXiv*

                14. Python for Beginners Course <https://www.youtube.com/watch?v=nLRL_NcnK-4>
                    *Free comprehensive Python course for beginners*

                15. End to End Chatbot Project With Deplyment <https://www.youtube.com/watch?v=iSh_USpOZP8&t=218s>
                    *(Flask, Claude , Langchain and Deployed on  Render)*

                16. RAG Explained <https://www.youtube.com/watch?v=NcCL1gJYyzw&t=11s>
                    *(Retrival Augmented Generation)*

                17. Industry ready Data Science Project | AI Project(RAG Chatbot playlist)<https://www.youtube.com/playlist?list=PLSdiMs6f-QAcGVpnZ1ougPScXkAuvqIU6>
                    *(Create a RAG based Chatbot following Industry Ready Project)

                18. What is AGI?<https://www.youtube.com/watch?v=2yAf_Ne6Br0&list=PLSdiMs6f-QAc4iqzR16jwELlKtrbySzEA&index=3&t=524s>
                    *(What is AGI?)

                19. End to End PowerBI Project<https://www.youtube.com/watch?v=IcU7qYBLu88&list=PLSdiMs6f-QAeOKeTIyMYKdUkFa_E4sIzx&index=3&t=2159s>
                    *(End to end power bi chatbot) 

                20. Movie Recommedation system AI Project with research paper implementation.<https://www.youtube.com/watch?v=R_D0uxRMD_c>
                    *(Movie Recommedation system with research paper implementation)

                21. End to End Nlp Playlist<https://www.youtube.com/playlist?list=PLSdiMs6f-QAdx_k-sjXEnhqq3ng-bAZIv>
                    *(NLP playlist)

                22. Python for data science Interview playlist<https://www.youtube.com/playlist?list=PLSdiMs6f-QAfs6yKWuKTZRE5YYLu4Yz7S>
                    *(Python Coding Question)

                23. SQL Coding Series<https://www.youtube.com/playlist?list=PLSdiMs6f-QAdig5qfO_z68Tf4SyhviUh1>
                    *(SQL coding series)

                24. Latest AI Developments<https://www.youtube.com/playlist?list=PLSdiMs6f-QAc4iqzR16jwELlKtrbySzEA>
                    *(Latest AI developments)
                If no relevant resources are available, say: "We'll add more resources soon. For urgent needs, please use this form: <https://forms.gle/DFCfRZroJvcmZQWRA>"

                25. AI Agents Playlist<https://www.youtube.com/playlist?list=PLSdiMs6f-QAe57Eq4-uADUdKfAJdgyxh0>
                    *(AI Agents playlist)

                26. Pytest Playlist<https://www.youtube.com/playlist?list=PLSdiMs6f-QAcdBZkR3B5FBdKPMwrJ7oxK>
                    *(Pytest playlist)

                27. AI System Design Playlist<https://www.youtube.com/watch?v=c4qVU8iH7ks&list=PLSdiMs6f-QAeHXcBFSuZo75wJd860dMxb>
                    *(AI System Design playlist)

                28. Deep Learning Project Playlist<https://www.youtube.com/watch?v=8XC6KXkmGrc&list=PLSdiMs6f-QAfxa_HhxIJR_K6UaWIISYar>
                    *(Deep Learning Projectplaylist)

                29. Pytorch Playlist<https://www.youtube.com/watch?v=qHfQqr6YoCQ&list=PLSdiMs6f-QAezDaYYhFAFu4ZXSeEegNHh&index=10>
                    *(Pytorch playlist)

                '''
            ),
            (
                'user',
                user_message
               
            )
        ]
        response =  await llm.ainvoke(message)

        await update.message.reply_text(response.content)
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        await update.message.reply_text("An error occurred while processing your message. Please try again later.")
    
    