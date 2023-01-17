import requests
import json
endpoint = "http://127.0.0.1:8000/import/"
data = {'Scenario': 1, 
        'Version': 1, 
        'data': {
            'Relationships': [
                {'__EMPTY': 0, 'Parent': 'USSH', 'Child': 'Braun, King and Barrows', 'Ownership Percentage': 0.6859
                },
                {'__EMPTY': 1, 'Parent': 'USSH', 'Child': 'Pacocha, Kemmer and Orn', 'Ownership Percentage': 1
                },
                {'__EMPTY': 2, 'Parent': 'USSH', 'Child': 'Mueller, Dach and Hyatt', 'Ownership Percentage': 1
                },
                {'__EMPTY': 3, 'Parent': 'USSH', 'Child': 'Konopelski - Dare', 'Ownership Percentage': 0.1666
                },
                {'__EMPTY': 4, 'Parent': 'USSH', 'Child': 'Collins, Gleason and Abshire', 'Ownership Percentage': 1
                },
                {'__EMPTY': 5, 'Parent': 'USSH', 'Child': 'Morissette - Steuber', 'Ownership Percentage': 0.0459
                },
                {'__EMPTY': 6, 'Parent': 'USSH', 'Child': 'Schroeder - Fritsch', 'Ownership Percentage': 0.2906
                },
                {'__EMPTY': 7, 'Parent': 'USSH', 'Child': 'Reynolds, Kozey and Kerluke', 'Ownership Percentage': 1
                },
                {'__EMPTY': 8, 'Parent': 'USSH', 'Child': "Schoen, O'Conner and Senger", 'Ownership Percentage': 0.5442
                },
                {'__EMPTY': 9, 'Parent': 'USSH', 'Child': 'Kovacek and Sons', 'Ownership Percentage': 1
                },
                {'__EMPTY': 10, 'Parent': 'USSH', 'Child': 'Schiller, Huels and Moen', 'Ownership Percentage': 0.2934
                },
                {'__EMPTY': 11, 'Parent': 'USSH', 'Child': 'Torp LLC', 'Ownership Percentage': 1
                },
                {'__EMPTY': 12, 'Parent': 'USSH', 'Child': 'Crona, Harris and Grimes', 'Ownership Percentage': 1
                },
                {'__EMPTY': 13, 'Parent': 'USSH', 'Child': 'Mraz - Frami', 'Ownership Percentage': 1
                },
                {'__EMPTY': 14, 'Parent': 'USSH', 'Child': 'Ferry Group', 'Ownership Percentage': 0.6916
                }
            ]
        }
            
    
    }

# requests.post(endpoint,json=data)



print(requests.post(endpoint,data).json())