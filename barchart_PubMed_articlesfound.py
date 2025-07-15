import matplotlib.pyplot as plt
import numpy as np

topics = ['other', 'radon', 'asthma', 'ETS']
articles = [19, 17, 7, 2]

plt.bar(topics, articles)
plt.yticks([0, 5, 10, 15, 20])
plt.xlabel('Topics')
plt.ylabel('Number of Articles')
plt.title('Number of PubMed Articles Found by Topic')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()