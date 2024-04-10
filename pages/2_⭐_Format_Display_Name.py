import streamlit as st
import pandas as pd

cnx=st.connection("snowflake")
session = cnx.session()

def get_user_profile_info():
   #start over with authentication and populating vars
   this_user_sql =  (f"select badge_given_name, badge_middle_name, badge_family_name, display_name, badge_email "
                     f"from UNI_USER_BADGENAME_BADGEEMAIL where UNI_ID=trim('{st.session_state.uni_id}') "
                     f"and UNI_UUID=trim('{st.session_state.uni_uuid}')")
   this_user_df = session.sql(this_user_sql)
   user_results_pd_df = this_user_df.to_pandas()                          
   user_rows = user_results_pd_df.shape[0]

   if user_rows>=1:       
      # 1 row found means the UNI_ID is legit and can be used to look up other information
      # all user vars need to be checked to make sure they aren't empty before we set session vars
      
      if user_results_pd_df['BADGE_GIVEN_NAME'].iloc[0] is not None:
         st.session_state['given_name'] = user_results_pd_df['BADGE_GIVEN_NAME'].iloc[0]  
         st.session_state['middle_name'] = user_results_pd_df['BADGE_MIDDLE_NAME'].iloc[0] #this is on purpose
      if user_results_pd_df['BADGE_FAMILY_NAME'].iloc[0] is not None:    
         st.session_state['family_name'] = user_results_pd_df['BADGE_FAMILY_NAME'].iloc[0]
      if user_results_pd_df['BADGE_EMAIL'].iloc[0] is not None:
         st.session_state['badge_email'] = user_results_pd_df['BADGE_EMAIL'].iloc[0]  
      if user_results_pd_df['DISPLAY_NAME'].iloc[0] is not None:
         st.session_state['display_name'] = user_results_pd_df['DISPLAY_NAME'].iloc[0]
      else:
         st.session_state['display_name'] = "PLEASE GO TO THE DISPLAY NAME TAB TO GENERATE A DISPLAY NAME FOR YOUR BADGE"
      st.dataframe(user_results_pd_df)
   else: # no rows returned
        st.markdown(":red[There is no record of the UNI_ID/UUID combination you entered. Please double-check the info you entered, check the FAQs tab below for tips on FINDING YOUR INFO, and try again]") 


st.subheader("Format the Display of Your Name for Your Badge(s)")

if st.session_state.auth_status == 'authed':
   with st.form("display_formatting"):
      display_option_1 = st.session_state.given_name.title() + " " + st.session_state.middle_name.capitalize() + " " + st.session_state.family_name.capitalize() #lazy do it for me
      display_option_2 = st.session_state.given_name.capitalize() + " " + st.session_state.middle_name.capitalize() + " " + st.session_state.family_name #european w nobiliary
      display_option_3 = st.session_state.family_name.upper() + " " + st.session_state.middle_name + " " + st.session_state.given_name.capitalize()  #east asian with alt script middle
      display_option_4 = st.session_state.family_name.upper() + " " +  st.session_state.given_name.capitalize() + " " + st.session_state.middle_name.capitalize() #east asian with alt script middle
      display_option_5 = st.session_state.given_name.capitalize() + " " +  st.session_state.middle_name.capitalize() + " " + st.session_state.family_name.upper() #ze french

      badge_name_order = st.radio("Name Display Order You Prefer:",                            
                                 [display_option_1, display_option_2, display_option_3, display_option_4, display_option_5],
                                  captions = ["Common in Anglo Traditions", "For names with nobiliary particles (van der, de la, von, zu, etc.)", "For use with dual script like 전 JEON Joon-kook 정국 ", "For cultures that put FAMILY name first", "Common for French and Francophonic"]
                                   )
      submit_display_format = st.form_submit_button("Record My Name Display Preference")

      if submit_display_format:
            if badge_name_order == display_option_1:
                display_format = 1
                edited_display_name = display_option_1     
            elif badge_name_order == display_option_2:
                display_format = 2
                edited_display_name = display_option_2    
            elif badge_name_order == display_option_3:
                display_format = 3
                edited_display_name = display_option_3         
            elif badge_name_order == display_option_4:
                display_format = 4
                edited_display_name = display_option_4
            elif badge_name_order == display_option_5:
                display_format = 5
                edited_display_name = display_option_5
            else: 
                st.write('Choose a format for your name')

            session.call('AMAZING.APP.UPDATE_BADGE_DISPLAYNAME_SP',st.session_state.uni_id, st.session_state.uni_uuid, display_format, edited_display_name)
            get_user_profile_info()
            st.success('Badge Display Name Updated', icon='🚀')
else: # not authed
   st.markdown(":red[Please sign in using your UNI_ID and UUID in the sidebar of the homepage.]")
 




