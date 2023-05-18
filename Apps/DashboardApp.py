import streamlit as st
import GetData
import plotly.express as px
import Utility


def dashboard_app():
    st.markdown("<h1 style='text-align: center;'>Mining Production Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<style>footer {visibility: hidden;}</style>", unsafe_allow_html=True)
    try:
        snow_obj = GetData.GetDataFromSnowflake(**st.secrets["snowflake"])
        df_date_flow = snow_obj.execute_query(Utility.query_data_flow)
        df_copper = snow_obj.execute_query(Utility.query_copper_refined)
        df_zinc = snow_obj.execute_query(Utility.query_zinc_mine)
    except Exception as e:
        st.error(e)
    else:
        try:
            if len(df_date_flow) > 0:
                fig_bar_copper_mine = px.bar(df_copper, y=df_copper['PRODUCTION_VALUE'],
                                             x=df_copper['PRODUCTION_DATE'],
                                             title='Production of copper, Refined',
                                             labels={'PRODUCTION_VALUE': 'Production Value (tonnes (metric))',
                                                     'PRODUCTION_DATE': 'Production Date'})
                fig_line_copper_mine = px.line(df_copper, y=df_copper["PRODUCTION_VALUE"],
                                               x=df_copper["PRODUCTION_DATE"],
                                               title='Production of copper, Refined',
                                               labels={'PRODUCTION_VALUE': 'Production Value (tonnes (metric))',
                                                       'PRODUCTION_DATE': 'Production Date'},
                                               markers=True)

                fig_bar_zinc_mine = px.bar(df_zinc, y=df_zinc['PRODUCTION_VALUE'], x=df_zinc['PRODUCTION_DATE'],
                                           title='Production of zinc, mine',
                                           labels={'PRODUCTION_VALUE': 'Production Value (tonnes (metal content))',
                                                   'PRODUCTION_DATE': 'Production Date'})
                fig_line_zinc_mine = px.line(df_zinc, y=df_zinc["PRODUCTION_VALUE"], x=df_zinc["PRODUCTION_DATE"],
                                             title='Production of zinc, mine',
                                             labels={'PRODUCTION_VALUE': 'Production Value (tonnes (metal content))',
                                                     'PRODUCTION_DATE': ' ProductionDate'},
                                             markers=True)

                fig_bar_zinc_mine.update_layout(Utility.layout)
                fig_bar_copper_mine.update_traces(marker_color='#3a92f0')
                fig_bar_copper_mine.update_xaxes(showgrid=False)
                fig_bar_copper_mine.update_yaxes(showgrid=False)

                fig_bar_copper_mine.update_layout(Utility.layout)
                fig_bar_zinc_mine.update_traces(marker_color='#3a92f0')
                fig_bar_zinc_mine.update_xaxes(showgrid=False)
                fig_bar_zinc_mine.update_yaxes(showgrid=False)

                fig_line_copper_mine.update_traces(line_color='#92fa23')
                fig_line_copper_mine.update_layout(Utility.layout)

                fig_line_zinc_mine.update_traces(line_color='#92fa23')
                fig_line_zinc_mine.update_layout(Utility.layout)

                left_col, right_col = st.columns(2)
                with left_col:
                    st.plotly_chart(fig_bar_copper_mine, use_container_width=True)
                    st.plotly_chart(fig_bar_zinc_mine, use_container_width=True)
                with right_col:
                    st.plotly_chart(fig_line_copper_mine, use_container_width=True)
                    st.plotly_chart(fig_line_zinc_mine, use_container_width=True)
            else:
                st.error('Data Not Available At Source Location, No Dashboards To Display 🧐')
        except Exception as e:
            st.error(e)
