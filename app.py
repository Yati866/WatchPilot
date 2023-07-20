import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import helper
import recommedation

netflix_df = pd.read_csv('netflix_titles.csv')
amazon_df = pd.read_csv('amazon_prime_titles.csv')
hotstar_df = pd.read_csv('disney_plus_titles.csv')
netflix_df['platform'] = 'netflix'
amazon_df['platform'] = 'amazon'
hotstar_df['platform'] = 'hotstar'

dataset = pd.concat([netflix_df,amazon_df,hotstar_df],ignore_index = True)

netflix_shows=netflix_df[netflix_df['type']=='TV Show']
netflix_movies=netflix_df[netflix_df['type']=='Movie']
amazon_shows=amazon_df[amazon_df['type']=='TV Show']
amazon_movies=amazon_df[amazon_df['type']=='Movie']
hotstar_shows=hotstar_df[hotstar_df['type']=='TV Show']
hotstar_movies=hotstar_df[hotstar_df['type']=='Movie']
dataset_shows=dataset[dataset['type']=='TV Show']
dataset_movies=dataset[dataset['type']=='Movie']

st.sidebar.title("Watch Pilot ⌚")
st.sidebar.image('Netflix-amazon-prime-video-disney-hotstar-collage.jpg')

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Content Distribution','Shows and Movies Timeline','Best releasing time','Yearwise Analysis','Duration Analysis','Top genres Analysis','Content Rating Analysis','Get Recommendations')
)

if user_menu == 'Content Distribution':
    # st.sidebar.header("Content Distribution")
    country_menu = st.sidebar.radio(
    'Select an Option',
    ('Country wise Content Distribution','Pie chart Overall Content Distribution','Bar Chart Overall Content Distribution')
)
    if country_menu == 'Country wise Content Distribution':
        selected_dataset = st.sidebar.selectbox("Select Dataset", ('Overall', 'Netflix', 'Hotstar', 'Amazon Prime'))
        if selected_dataset == 'Overall':
           country_df = dataset
        elif selected_dataset == 'Netflix':
            country_df = netflix_df
        elif selected_dataset == 'Hotstar':
            country_df = hotstar_df
        elif selected_dataset == 'Amazon Prime':
            country_df = amazon_df
        country = helper.get_unique_countries(country_df)
        selected_country = st.sidebar.selectbox("Select Country", country)
        st.title("Content Tally of " + str(selected_country) + " " + str(selected_dataset))
        palette = ['Blue', 'Black']
        fig = helper.generate_content_type_distribution(country_df, selected_country, palette)
        if fig is not None:
           st.pyplot(fig)
    elif country_menu == 'Pie chart Overall Content Distribution':
        helper.generate_platform_content_pie_charts(dataset)
    elif country_menu == 'Bar Chart Overall Content Distribution':
        helper.generate_content_type_bar_distribution(netflix_df, amazon_df, hotstar_df)

if user_menu == 'Shows and Movies Timeline':
    time_chart_option = st.sidebar.radio(
    'Select an Option',
    ('Movies', 'TV Shows')
)
    st.subheader("Analysis Note")
    st.markdown("Since this dataset is till 2021 only but we can say that by 2021 netflix"
                 "is more prone to release tv-shows then movies but amazon has released more movies than shows and hotstar has done more shows")
    if time_chart_option == 'Movies':
       helper.generate_movies_by_year_plot(dataset)
    elif time_chart_option == 'TV Shows':
       helper.generate_shows_by_year_plot(dataset)

if user_menu == 'Best releasing time':
    release_chart_option = st.sidebar.radio(
    'Select an Option',
    ('Movies', 'TV Shows')
)
    st.subheader("Analysis Note")
    st.markdown("Understanding the best releasing time for movies and TV shows can help optimize viewership. "
                "Here we analyze the release patterns of Netflix movies and TV shows to identify trends and insights.")
    if release_chart_option == 'Movies':
       helper.generate_netflix_movies_update_heatmap(netflix_df)
    elif release_chart_option == 'TV Shows':
       helper.generate_netflix_shows_update_heatmap(netflix_df)

if user_menu == 'Yearwise Analysis':
    year_chart_option = st.sidebar.radio(
    'Select an Option',
    ('Movies', 'TV Shows')
)
    st.subheader("Analysis Note")
    st.markdown("Understanding the Year wise analysis for of differnt platform shows and movie release "
                "we observe that with the increasing year publishing rate is also increasing.")
    if year_chart_option == 'Movies':
       st.subheader("Movies and Year")
       ax = helper.generate_movies_release_year_bar_plot(dataset)
       st.pyplot(ax.figure)
    elif year_chart_option == 'TV Shows':
       st.subheader("Shows and Year")
       ax = helper.generate_shows_release_year_bar_plot(dataset)
       st.pyplot(ax.figure)

if user_menu == 'Duration Analysis':
    dur_menu = st.sidebar.radio(
    'Select an Option',
    ('Movies duration charts','Best movies w.r.t. durations','Season Analysis')
)
    if dur_menu == 'Movies duration charts':
        st.subheader("Duration of movies of differnt platform")
        st.markdown("A good amount of movies are among the duration of 75-120 mins. 😯")
        helper.generate_movies_duration_distribution(netflix_movies, amazon_movies, hotstar_movies)
    
    if dur_menu == 'Best movies w.r.t. durations':
        selected_dataset = st.sidebar.selectbox("Select Dataset", ('All','Netflix', 'Hotstar', 'Amazon Prime'))
        if selected_dataset == 'Netflix':
           st.subheader("Netflix best movies with respect to durations")
           fig = helper.top10_max_duration_movies_barplot(netflix_movies)
        elif selected_dataset == 'Amazon Prime':
            st.subheader("Prime best movies with respect to durations")
            fig = helper.top10_max_duration_movies_barplot(amazon_movies)
        elif selected_dataset == 'Hotstar':
            st.subheader("Hotstar best movies with respect to durations")
            fig = helper.top10_max_duration_movies_barplot(hotstar_movies)
        elif selected_dataset == 'All':
            st.subheader("Overall best movies with respect to durations")
            st.markdown("Are you able to find your good movies now 😒😒")
            fig = helper.top10_max_duration_movies_barplot(dataset_movies)
        st.pyplot(fig)
    
    if dur_menu == 'Season Analysis':
        selected_dataset = st.sidebar.selectbox("Select Dataset", ('All','Netflix', 'Hotstar', 'Amazon Prime'))
        if selected_dataset == 'Netflix':
           st.subheader("Netflix best shows with respect to durations")
           fig = helper.top10_max_duration_season_barplot(netflix_shows)
        elif selected_dataset == 'Amazon Prime':
            st.subheader("Prime best shows with respect to durations")
            fig = helper.top10_max_duration_season_barplot(amazon_shows)
        elif selected_dataset == 'Hotstar':
            st.subheader("Hotstar best shows with respect to durations")
            fig = helper.top10_max_duration_season_barplot(hotstar_shows)
        elif selected_dataset == 'All':
            st.subheader("Overall best movies with respect to durations")
            st.markdown("Are you able to find your good shows now 😒😒")
            fig = helper.top10_max_duration_season_barplot(dataset_shows)
        st.pyplot(fig)
if user_menu == 'Top genres Analysis':
    selected_dataset = st.sidebar.selectbox("Select Dataset", ('Netflix', 'Amazon Prime', 'Hotstar'))

    df_group_genre = dataset.groupby(['platform', 'listed_in', 'type']).count()['show_id'].reset_index()

    if selected_dataset == 'Netflix':
        st.subheader("Top 10 genres on Netflix")
        netflix_top_genres = df_group_genre[df_group_genre['platform'] == 'netflix'].sort_values('show_id', ascending=False)[:10]
        styled_table_netflix = netflix_top_genres.style.background_gradient()
        top10_netflix = netflix_top_genres['listed_in'].values.tolist()
        filtered_data = dataset[(dataset['platform'] == 'netflix') & (dataset['listed_in'].isin(top10_netflix))]
    elif selected_dataset == 'Amazon Prime':
        st.subheader("Top 10 genres on Amazon Prime")
        amazon_top_genres = df_group_genre[df_group_genre['platform'] == 'amazon'].sort_values('show_id', ascending=False)[:10]
        styled_table_amazon = amazon_top_genres.style.background_gradient()
        top10_amazon = amazon_top_genres['listed_in'].values.tolist()
        filtered_data = dataset[(dataset['platform'] == 'amazon') & (dataset['listed_in'].isin(top10_amazon))]
    elif selected_dataset == 'Hotstar':
        st.subheader("Top 10 genres on Hotstar")
        hotstar_top_genres = df_group_genre[df_group_genre['platform'] == 'hotstar'].sort_values('show_id', ascending=False)[:10]
        styled_table_hotstar = hotstar_top_genres.style.background_gradient()
        top10_hotstar = hotstar_top_genres['listed_in'].values.tolist()
        filtered_data = dataset[(dataset['platform'] == 'hotstar') & (dataset['listed_in'].isin(top10_hotstar))]

    genre_counts = filtered_data['listed_in'].value_counts()

    plt.figure(figsize=(4, 4))
    sns.set_palette('Set2')
    plt.pie(genre_counts, labels=genre_counts.index, autopct='%1.1f%%', startangle=90)

    if selected_dataset == 'Netflix':
        plt.title('Top 10 genres on Netflix', fontweight='bold', fontsize=14)
    elif selected_dataset == 'Amazon Prime':
        plt.title('Top 10 genres on Amazon Prime', fontweight='bold', fontsize=14)
    elif selected_dataset == 'Hotstar':
        plt.title('Top 10 genres on Hotstar', fontweight='bold', fontsize=14)

    plt.axis('equal')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()

if user_menu == 'Content Rating Analysis':
    fig = helper.plot_content_rating(dataset)
    st.pyplot(fig)

if user_menu == 'Get Recommendations':
    titles = recommedation.get_titles(dataset)
    selected_titles = st.sidebar.selectbox("Select Movie or shows titles", titles)
    if st.sidebar.button("Get Recommendations"):
        # Get recommendations and platforms based on the selected title
        recommended_df = recommedation.get_recommendations_with_platform(dataset, selected_titles)

        # Display the recommendations with platforms in a box-like format
        st.title("Recommended Shows and Movies")
        st.dataframe(recommended_df)




    


        









        

    

    
    
