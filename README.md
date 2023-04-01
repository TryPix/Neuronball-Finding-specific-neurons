# Neuronball-Finding-Specific-neurons

Neuronball is an online multiplayer game where two teams of 5 "neurons" face of in a football style simulation. Each neuron has a name, which usually composed of a prefix and suffix. There are a large amount of these prefix-suffix combinations, and the goal is to find Neurons with a specific prefix name, by crawling through all the neurons.

Each neuron is uniquely indexed by an id, and can be found on _neuronball.com/player/<neuron_id>/_.

The scrapy framework is used to fetch the html code as text, from which one can search if neuron has the wanted characteristics. In the example provided, we search for neurons with the prefix "Cobra" which are not of type "Standard". 

DISCLAIMER: As the number of neurons is pretty significant, it not recommended to crawl on every neuron-website in one go.

