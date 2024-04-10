import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col

cnx=st.connection("snowflake")
session = cnx.session()

st.subheader(":robot_face: View All DORA Tests You Have Run in the Last 90 Days")
st.write("Click on column headings to sort. Use the drop list to filter the checks to just a single workshop.")
st.write("You can search the table of results by rolling your cursor over the header and choosing the magnifying lens symbol.")
        
if st.session_state.auth_status == 'authed':
        mw_choice = st.selectbox("Filter to show workshop records for:", ("DWW", "CMCW", "DABW", "DLKW", "DNGW" ))
        passed_valid = st.radio(
                            "Which tests do you want to see?",
                                ["All Tests", "Only Passed", "Only Passed & Valid"],
                            index=0,
        )

        st.write("You have chosen to see:", passed_valid)

        
        if mw_choice:
                all_my_tests_df = session.table("AMAZING.APP.ALL_MY_TESTS").filter((col('uni_id')== st.session_state.uni_id) & (col('badge_acro')== mw_choice))
                all_my_tests_pd_df = all_my_tests_df.to_pandas()
                amt_rows = all_my_tests_pd_df.shape[0]
                st.dataframe(all_my_tests_pd_df)
                        
                if amt_rows > 0:    
                        if passed_valid == "All Tests":
                                filtered_df = all_my_tests_pd_df
                        elif passed_valid == "Only Passed":
                                # st.dataframe(all_my_tests_pd_df.filter(col("passed")==TRUE))
                                filtered_df = all_my_tests_df[all_my_tests_df["passed"].str.contains("True")]
                                # df.filter((col("A") > 1) & (col("B") < 100))
                        elif passed_valid == "Only Passed & Valid":
                                filtered_df = all_my_tests_pd_df
                        else:
                                filtered_df = all_my_tests_pd_df
                        st.dataframe(filtered_df
                                , column_order=["STEP","ACCOUNT_LOCATOR","PASSED", "DORA_TIMESTAMP", "LEARNER_SENT"]
                                , column_config={ 
                                "STEP": "DORA Check #"
                                ,"ACCOUNT_LOCATOR": "Acct Loc"
                                , "PASSED": "Passed"
                                ,"DORA_TIMESTAMP": "Submission Date/Time"
                                ,"LEARNER_SENT": "Check Details"},    
                                hide_index=True,
                                height=1200
                        )

else: # not authed
   st.markdown(":red[Please sign in using your UNI_ID and UUID in the sidebar of the homepage.]")                                        

