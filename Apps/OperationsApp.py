import streamlit as st
import GetData
import plotly.express as px
import Utility


def operations_app():
    st.markdown("<h1 style='text-align: center;'>Data Operations Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<style>footer {visibility: hidden;}</style>", unsafe_allow_html=True)
    try:
        snow_obj = GetData.GetDataFromSnowflake(**st.secrets["snowflake"])
        df_date_flow = snow_obj.execute_query(Utility.query_data_flow)
    except Exception as e:
        st.error(e)
    else:
        try:
            if len(df_date_flow) > 0:
                df_date_flow_bar = df_date_flow[df_date_flow['LABEL'] != 'ERRONEOUS RECORDS']
                df_date_flow_pie = df_date_flow[df_date_flow['LABEL'] != 'SOURCE RECORDS']

                fig_bar_data_flow = px.bar(df_date_flow_bar, y=df_date_flow_bar['RECORDS_COUNT'],
                                           x=df_date_flow_bar['LABEL'],
                                           title='Data Flow',
                                           labels={'RECORDS_COUNT': 'Records Count',
                                                   'LABEL': 'Label'})

                fig_pie_null_clean_records = px.pie(df_date_flow_pie, values="RECORDS_COUNT",
                                                    names="LABEL",
                                                    title="Data Flow"
                                                    )
                fig_pie_null_clean_records.update_traces(marker=dict(colors=['green', 'red']))

                fig_pie_null_clean_records.update_layout(Utility.layout)

                fig_bar_data_flow.update_layout(Utility.layout)
                fig_bar_data_flow.update_traces(marker_color='#3a92f0')
                fig_bar_data_flow.update_xaxes(showgrid=False)
                fig_bar_data_flow.update_yaxes(showgrid=False)

                left_col, right_col = st.columns(2)
                with left_col:
                    st.plotly_chart(fig_pie_null_clean_records, use_container_width=True)
                with right_col:
                    st.plotly_chart(fig_bar_data_flow, use_container_width=True)
            else:
                st.error('Statistics Data Not Available At Source Location, No Dashboards To Display 🧐')
        except Exception as e:
            st.error(e)
