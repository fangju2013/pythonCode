# -*- coding: utf-8 -*-

from math import sqrt

dataset={
			'Lisa Rose': {'Lady in the Water': 2.5,
							'Snakes on a Plane': 3.5,
							'Just My Luck': 3.0,
							'Superman Returns': 3.5,
							'You, Me and Dupree': 2.5,
							'The Night Listener': 3.0},
			'Gene Seymour': {'Lady in the Water': 3.0,
							'Snakes on a Plane': 3.5,
							'Just My Luck': 1.5,
							 'Superman Returns': 5.0,
							 'The Night Listener': 3.0,
							'You, Me and Dupree': 3.5},

			'Michael Phillips': {'Lady in the Water': 2.5,
								'Snakes on a Plane': 3.0,
								'Superman Returns': 3.5,
								 'The Night Listener': 4.0},
			'Claudia Puig': {'Snakes on a Plane': 3.5,
							'Just My Luck': 3.0,
							'The Night Listener': 4.5,
							'Superman Returns': 4.0,
							'You, Me and Dupree': 2.5},
			'Mick LaSalle': {'Lady in the Water': 3.0,
							'Snakes on a Plane': 4.0,
							'Just My Luck': 2.0,
							'Superman Returns': 3.0,
							'The Night Listener': 3.0,
							'You, Me and Dupree': 2.0},
			'Jack Matthews': {'Lady in the Water': 3.0,
							'Snakes on a Plane': 4.0,
							'The Night Listener': 3.0,
							'Superman Returns': 5.0,
							'You, Me and Dupree': 3.5},
			'Toby': {'Snakes on a Plane':4.5,
					'You, Me and Dupree':1.0,
					'Superman Returns':4.0}}

def similarity_score(person1,person2):
    both_viewed={}
    for item in dataset[person1]:
        if item in dataset[person2]:
            both_viewed[item]=1
        if len(both_viewed)==0:
            return 0
        sum_of_eclidean_distance=[]
        for item in dataset[person1]:
            if item in dataset[person2]:
                sum_of_eclidean_distance.append(pow(dataset[person1]-dataset[person2],2))
        sum_of_eclidean_distance=sum(sum_of_eclidean_distance)
    return 1/(1+sqrt(sum_of_eclidean_distance))

def pearson_correlation(person1,person2):
    both_rated={}
    for item in dataset[person1]:
        if item in dataset[person2]:
            both_rated[item]=1
    number_of_ratings=len(both_rated)
    if number_of_ratings==0:
        return 0
    person1_preferences_sum=sum([dataset[person1][item] for item in both_rated])
    person2_preferences_sum=sum([dataset[person2][item] for item in both_rated])
    person1_square_preferences_sum=sum([pow(dataset[person1][item],2) for item in both_rated])
    person2_square_preferences_sum=sum([pow(dataset[person2][item],2) for item in both_rated])
    product_sum_of_both_users=sum([dataset[person1][item]*dataset[person2][item] for item in both_rated])
    numerator_value=product_sum_of_both_users-(person1_preferences_sum*person2_preferences_sum/number_of_ratings)
    denominator_value=sqrt((person1_square_preferences_sum-pow(person1_preferences_sum,2)/number_of_ratings)*\
                           (person2_square_preferences_sum-pow(person2_preferences_sum,2)/number_of_ratings))
    if denominator_value==0:
        return 0
    else:
        r=numerator_value/denominator_value
        return r

def most_similar_users(person,number_of_users):
    scores=[(pearson_correlation(person,other_person),other_person) for other_person in dataset if other_person !=person]
    scores.sort()
    scores.reverse()
    return scores[0:number_of_users]

def user_recommendations(person):
    totals={}
    simSums={}
    rankings_list=[]
    for other in dataset:
        if other==person:
            continue
        sim=pearson_correlation(person,other)
        if sim<0:
            continue
        for item in dataset[other]:
            if item not in dataset[person] or dataset[person][item]==0:
                totals.setdefault(item,0)
                totals[item]+=dataset[other][item]*sim
                simSums.setdefault(item,0)
                simSums[item]+=sim
    rankings=[(total/simSums[item],item) for item,total in totals.items()]
    rankings.sort()
    rankings.reverse()
    recommendations_list=[recommend_item for score,recommend_item in rankings]
    return recommendations_list

print user_recommendations('Toby')