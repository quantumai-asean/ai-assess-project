# Project Planning

[ ] create [dev.container](https://github.com/devcontainers/templates/tree/main/src/anaconda-postgres) 

[✅] create conda env (py 3.11)

[✅] install model-card-toolkit, streamlit

* install [bazel](https://bazel.build/install/ubuntu)
* install model-card-toolkit from [source](https://www.tensorflow.org/responsible_ai/model_card_toolkit/guide/install#installing_from_source)

[ ] make a streamlit UI that configures a modelcard; 
* supportive components: [streamlit-pydantic](https://github.com/lukasmasuch/streamlit-pydantic#examples), install pydantic from source
* how to create multi-page app [doc](https://docs.streamlit.io/library/advanced-features/multipage-apps),[blog](https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app)
* [statefull app, useful for multipage](https://docs.streamlit.io/library/advanced-features/session-state)
* [pydantic doc](https://docs.pydantic.dev/latest/concepts/models/#arbitrary-class-instances)

[✅] Display MC report with the UI?

[ ] save data to file before using database
* use postgresql
* how to add uuid as key to a table?:

                # add extension to generate uuid
                CREATE EXTENSION IF NOT EXISTS "uuid-ossp"; 
                
                #create a table with id as primary key, add constraint to be unique on selected column(s), and automatically generate UUID, e.g.
                CREATE TABLE owner (                                                     
                    name            varchar(40),
                    contact             varchar(60),
                    id SERIAL PRIMARY KEY, # unique running sequence as key
                    hash_key UUID DEFAULT uuid_generate_v4() UNIQUE # automatically genearte UUID 
                );
                ALTER TABLE owner ADD CONSTRAINT your_table_unique_constraint UNIQUE (name); #unique on selected column(s)
* install python psql module such as psycopg

[ ] install other assessment libraries: fairlearn, aequitas

[ ] 
        

## note to dev workflow in GitHub codespaces:
* use conda env "/workspaces/ai-assess-project/.conda"

# References
## Toolkits and Frameworks
* Microsoft RAI Toolbox [Homepage](https://responsibleaitoolbox.ai/) | [Tools and Practices](https://www.microsoft.com/en-us/ai/tools-practices) | [workshop](https://github.com/microsoft/responsible-ai-workshop) | [Github Repo](https://github.com/microsoft/responsible-ai-toolbox) + [JupyterLab Extension](https://github.com/microsoft/responsible-ai-toolbox-tracker) | [Robust ML](https://github.com/microsoft/robustlearn) | [AzureML](https://github.com/Azure/RAI-vNext-Preview) | [Mapping of Azure AI Sevices and RAI concerns](https://learn.microsoft.com/en-us/azure/ai-services/responsible-use-of-ai-overview) | [Azure BestPractices TrustedAI Framework](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/innovate/best-practices/trusted-ai)
* MIT AI Lab [Documentation](https://mit-ll-responsible-ai.github.io/responsible-ai-toolbox/) | [Github](https://github.com/mit-ll-responsible-ai/responsible-ai-toolbox/)
* SG AI Foundation AI Verify [Repo](https://github.com/IMDA-BTG/aiverify) | [UserGuide](https://imda-btg.github.io/aiverify/introduction/how-it-works/) [DeveloperDoc](https://imda-btg.github.io/aiverify-developer-tools/), [StockPlugins](https://imda-btg.github.io/aiverify-developer-tools/stock_plugins/)
* Google [Tensorflow RAI Toolkit ***](https://www.tensorflow.org/responsible_ai) | [GoogleIO Build with RAI](https://io.google/2021/session/3a44428c-f3b8-4b42-a90b-20271d81e477/?lng=en) | [Toolify on the Same Toolkit](https://www.toolify.ai/ai-news/creating-ai-for-a-better-future-responsible-ai-toolkit-25702)
* OECD [Report: Regulatory sandboxes in artificial intelligence](https://oecd.ai/en/sandboxes) [site](https://www.oecd.org/sti/regulatory-sandboxes-in-artificial-intelligence-8f80a0e6-en.htm)
* Awesone RAI Repo [AthenaCore Awesome List](https://github.com/AthenaCore/AwesomeResponsibleAI) | [HolisticAI](https://github.com/holistic-ai) | [VerifyML](https://github.com/cylynx/verifyml) | [Ethical AI Production ML ***](https://github.com/EthicalML/awesome-production-machine-learning)
* InterpretML [home](https://interpret.ml) | [repo](https://github.com/interpretml/interpret) | [community-repo](https://github.com/interpretml/interpret-community)
* [Linux Foundation AI and Data Robustness Adversarial Toolbox](https://github.com/Trusted-AI/adversarial-robustness-toolbox)
* [Turing Report](https://www.turing.ac.uk/sites/default/files/2019-06/understanding_artificial_intelligence_ethics_and_safety.pdf)


