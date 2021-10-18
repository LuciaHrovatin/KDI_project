# KDI_project
Project repository for the course in Knowledge and Data Integration, academic year 2021/2022

Structure of json data from Twitter:
Useful stuff:
- When created:
"created_at": "Sun Oct 17 12:11:21 +0000 2021", # when the tweet has been posted
- Text:
"full_text": "RT @VisitTrentino: \ud83c\uddec\ud83c\udde7\nThe wineries of the Piana Rotaliana have a surprise in store for you! A journey through the history and transformatio\u2026",
- Interessante parte sulle entities!!!
"entities": {
    "hashtags": [],
    "symbols": [],
    "user_mentions": [
      {
        "screen_name": "VisitTrentino",
        "name": "Visit Trentino",
        "id": 124874351,
        "id_str": "124874351",
        "indices": [
          3,
          17
        ]
      }
    ],
    "urls": []
  },
  "metadata": {
    "iso_language_code": "en",
    "result_type": "recent"
  },
  "source": "<a href=\"http://twitter.com/#!/download/ipad\" rel=\"nofollow\">Twitter for iPad</a>",
  "in_reply_to_status_id": null,
  "in_reply_to_status_id_str": null,
  "in_reply_to_user_id": null,
  "in_reply_to_user_id_str": null,
  "in_reply_to_screen_name": null,
  "user": {
    "id": 4747171347,
    "id_str": "4747171347",
    "name": "Donald Jensen",
    "screen_name": "donaldnjensen",
    "location": "",
    "description": "Director, Russia and Strategic Stability @USIP; Sonoma County rooted; Editor, Base Ball 12 (McFarland 2021); SF Giants, Juventus, 49ers, Columbia football fan",
    "url": null,
    "entities": {
      "description": {
        "urls": []
      }
    },
    "protected": false,
    "followers_count": 1044,
    "friends_count": 1324,
    "listed_count": 86,
    "created_at": "Fri Jan 08 19:22:35 +0000 2016",
    "favourites_count": 4011,
    "utc_offset": null,
    "time_zone": null,
    "geo_enabled": false,
    "verified": false,
    "statuses_count": 49827,
    "lang": null,
    "contributors_enabled": false,
    "is_translator": false,
    "is_translation_enabled": false,
    "profile_background_color": "F5F8FA",
    "profile_background_image_url": null,
    "profile_background_image_url_https": null,
    "profile_background_tile": false,
    "profile_image_url": "http://pbs.twimg.com/profile_images/685542642655039488/aBg2JIR3_normal.png",
    "profile_image_url_https": "https://pbs.twimg.com/profile_images/685542642655039488/aBg2JIR3_normal.png",
    "profile_banner_url": "https://pbs.twimg.com/profile_banners/4747171347/1452281497",
    "profile_link_color": "1DA1F2",
    "profile_sidebar_border_color": "C0DEED",
    "profile_sidebar_fill_color": "DDEEF6",
    "profile_text_color": "333333",
    "profile_use_background_image": true,
    "has_extended_profile": false,
    "default_profile": true,
    "default_profile_image": false,
    "following": false,
    "follow_request_sent": false,
    "notifications": false,
    "translator_type": "none",
    "withheld_in_countries": []
  },
  "geo": null,
  "coordinates": null,
  "place": null,
  "contributors": null,
  "retweeted_status": {
    "created_at": "Sun Oct 17 07:55:00 +0000 2021",
    "id": 1449645102754721792,
    "id_str": "1449645102754721792",
    "full_text": "\ud83c\uddec\ud83c\udde7\nThe wineries of the Piana Rotaliana have a surprise in store for you! A journey through the history and transformation of wine, combined with trekking, walks and the warm hospitality of Trentino!\n\u27a1\ufe0f https://t.co/XLN1WCSz8R\n\n[\ud83d\udccd@dolomitipaganel | \ud83d\udcf7 P. Lab]\n#visittrentino https://t.co/J55wgmndbr",
    "truncated": false,
    "display_text_range": [
      0,
      272
    ],
    "entities": {
      "hashtags": [
        {
          "text": "visittrentino",
          "indices": [
            258,
            272
          ]
        }
      ],
      "symbols": [],
      "user_mentions": [
        {
          "screen_name": "dolomitipaganel",
          "name": "Dolomiti Paganella",
          "id": 406337643,
          "id_str": "406337643",
          "indices": [
            229,
            245
          ]
        }
      ],
      "urls": [
        {
          "url": "https://t.co/XLN1WCSz8R",
          "expanded_url": "http://tinyurl.com/EnoturLABen",
          "display_url": "tinyurl.com/EnoturLABen",
          "indices": [
            202,
            225
          ]
        }
      ],
      "media": [
        {
          "id": 1448550271995547652,
          "id_str": "1448550271995547652",
          "indices": [
            273,
            296
          ],
          "media_url": "http://pbs.twimg.com/media/FBpIzDGXEAQxabu.jpg",
          "media_url_https": "https://pbs.twimg.com/media/FBpIzDGXEAQxabu.jpg",
          "url": "https://t.co/J55wgmndbr",
          "display_url": "pic.twitter.com/J55wgmndbr",
          "expanded_url": "https://twitter.com/VisitTrentino/status/1449645102754721792/photo/1",
          "type": "photo",
          "sizes": {
            "small": {
              "w": 680,
              "h": 510,
              "resize": "fit"
            },
            "thumb": {
              "w": 150,
              "h": 150,
              "resize": "crop"
            },
            "large": {
              "w": 1440,
              "h": 1080,
              "resize": "fit"
            },
            "medium": {
              "w": 1200,
              "h": 900,
              "resize": "fit"
            }
          }
        }
      ]
    },
    "extended_entities": {
      "media": [
        {
          "id": 1448550271995547652,
          "id_str": "1448550271995547652",
          "indices": [
            273,
            296
          ],
          "media_url": "http://pbs.twimg.com/media/FBpIzDGXEAQxabu.jpg",
          "media_url_https": "https://pbs.twimg.com/media/FBpIzDGXEAQxabu.jpg",
          "url": "https://t.co/J55wgmndbr",
          "display_url": "pic.twitter.com/J55wgmndbr",
          "expanded_url": "https://twitter.com/VisitTrentino/status/1449645102754721792/photo/1",
          "type": "photo",
          "sizes": {
            "small": {
              "w": 680,
              "h": 510,
              "resize": "fit"
            },
            "thumb": {
              "w": 150,
              "h": 150,
              "resize": "crop"
            },
            "large": {
              "w": 1440,
              "h": 1080,
              "resize": "fit"
            },
            "medium": {
              "w": 1200,
              "h": 900,
              "resize": "fit"
            }
          }
        }
      ]
    },
    "metadata": {
      "iso_language_code": "en",
      "result_type": "recent"
    },
    "source": "<a href=\"https://mobile.twitter.com\" rel=\"nofollow\">Twitter Web App</a>",
    "in_reply_to_status_id": null,
    "in_reply_to_status_id_str": null,
    "in_reply_to_user_id": null,
    "in_reply_to_user_id_str": null,
    "in_reply_to_screen_name": null,
    "user": {
      "id": 124874351,
      "id_str": "124874351",
      "name": "Visit Trentino",
      "screen_name": "VisitTrentino",
      "location": "Trentino",
      "description": "Trentino Tourism official account - Italy. Share with us #visittrentino & #trentinowow #lamiaterranonsiferma",
      "url": null,
      "entities": {
        "description": {
          "urls": []
        }
      },
      "protected": false,
      "followers_count": 35084,
      "friends_count": 276,
      "listed_count": 473,
      "created_at": "Sat Mar 20 21:57:16 +0000 2010",
      "favourites_count": 11748,
      "utc_offset": null,
      "time_zone": null,
      "geo_enabled": true,
      "verified": false,
      "statuses_count": 23604,
      "lang": null,
      "contributors_enabled": false,
      "is_translator": false,
      "is_translation_enabled": false,
      "profile_background_color": "131516",
      "profile_background_image_url": "http://abs.twimg.com/images/themes/theme1/bg.png",
      "profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme1/bg.png",
      "profile_background_tile": false,
      "profile_image_url": "http://pbs.twimg.com/profile_images/1374654556597018628/_h6iOxdq_normal.jpg",
      "profile_image_url_https": "https://pbs.twimg.com/profile_images/1374654556597018628/_h6iOxdq_normal.jpg",
      "profile_banner_url": "https://pbs.twimg.com/profile_banners/124874351/1614698041",
      "profile_link_color": "1B95E0",
      "profile_sidebar_border_color": "FFFFFF",
      "profile_sidebar_fill_color": "DDEEF6",
      "profile_text_color": "333333",
      "profile_use_background_image": true,
      "has_extended_profile": true,
      "default_profile": false,
      "default_profile_image": false,
      "following": false,
      "follow_request_sent": false,
      "notifications": false,
      "translator_type": "none",
      "withheld_in_countries": []
    },
    "geo": null,
    "coordinates": null,
    "place": null,
    "contributors": null,
    "is_quote_status": false,
    "retweet_count": 1,
    "favorite_count": 15,
    "favorited": false,
    "retweeted": false,
    "possibly_sensitive": false,
    "lang": "en"
  },
  "is_quote_status": false,
  "retweet_count": 1,
  "favorite_count": 0,
  "favorited": false,
  "retweeted": false,
  "lang": "en"
}