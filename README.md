# Project Planning

[✅] use dev container, create conda env (py 3.11)

[✅] install model-card-toolkit, streamlit

* install [bazel](https://bazel.build/install/ubuntu)
* install model-card-toolkit from [source](https://www.tensorflow.org/responsible_ai/model_card_toolkit/guide/install#installing_from_source)

[✅] make a streamlit UI that configures a modelcard; 
* supportive components: [streamlit-pydantic](https://github.com/lukasmasuch/streamlit-pydantic#examples), install pydantic from source
* how to create multi-page app [doc](https://docs.streamlit.io/library/advanced-features/multipage-apps),[blog](https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app)
* [statefull app, useful for multipage](https://docs.streamlit.io/library/advanced-features/session-state)
* [pydantic doc](https://docs.pydantic.dev/latest/concepts/models/#arbitrary-class-instances)
* try to use Frontend to do the assessment first, then move compute to backend
[✅] Display MC report with the UI?

[ ] save data to file before using database
* use postgresql
* how to add uuid as key to a table?:

                # add extension to generate uuid
                CREATE EXTENSION IF NOT EXISTS "uuid-ossp"; 
                
                #create a table with id as primary key, add constraint to be unique on selected column(s), and automatically generate UUID, e.g.
                CREATE TABLE owner (                                                     
                    name            varchar(40) NOT NULL,
                    contact             varchar(60),
                    id SERIAL PRIMARY KEY, # unique running sequence as key
                    hash_key UUID DEFAULT uuid_generate_v4() UNIQUE # automatically genearte UUID 
                );
                #ALTER TABLE owner ADD CONSTRAINT your_table_unique_constraint UNIQUE (name); #unique on selected column(s)
                
                CREATE UNIQUE INDEX your_table_unique_constraint ON owner (LOWER(name));
* install python psql module such as psycopg

[ ] install other assessment libraries: fairlearn, robustness by perturbation (AI Verify)?, ...

[ ] save protofile report to database and show them

[ ] try to use VerifyML model card toolkir src to modify report template
        
[ ] GenAI to summarise and comment assessment filing - https://ai.google.dev/tutorials/python_quickstart
## note to dev workflow in GitHub codespaces:
* use conda env "/workspaces/ai-assess-project/.conda"

# References
[my repos](https://github.com/quantumai-asean/AI-Ethics-Assessment-Project/blob/main/REFERENCES.md)

## Cloud Deployment
1. build docker image and install all depencies there
2. deploy compressed source files (using "zip -r app.zip .") with "az webapp deploy --name qai-rai-beta --resource-group sengtak_rg_3983 --src-path app.zip"
3. use starup command in Configuration "python -m streamlit run frontend/index.py --server.port 8000 --server.address 0.0.0.0"
4. Enable CORS with wildcard origin *
5. Add VNet Integration to App



