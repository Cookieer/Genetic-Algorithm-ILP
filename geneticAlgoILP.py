from random import sample
from random import randint
from random import floor
import rake_nltk

class GeneticAlgorithm:

  def __init__(self, AllSentences, summary, scores_sent, L):
    self.AllSentences = AllSentences
    self.summary = summary
    self.scores_sent = scores_sent
    self.rankedPhrases = self.getRankedPhrases(self.AllSentences)
    self.l = []
    for sent in self.summary:
      self.l.append(len(sent.split()))
    self.L = L
    self.individual_size = len(self.summary)
    self.population_size = 1000
    self.selection_size = floor(0.1 * self.population_size)
    self.max_generations = 50
    self.probability_of_individual_mutating = 0.1
    self.probability_of_gene_mutating = 0.25
    self.best_individuals_stash = [self.create_individual(self.individual_size)]
    self.THRESHOLD = 10
    self.initial_population = self.create_population(self.individual_size, 1000)
    self.current_population = self.initial_population
    self.termination = False
    self.generation_count = 0


  def getRankedPhrases(self, AllSentences):
    text = ''
    for s in AllSentences:
      text += s + ' '

    from rake_nltk import Rake
    r = Rake() 
    r.extract_keywords_from_text(text)
    rankedPhrases = r.get_ranked_phrases_with_scores()
    return rankedPhrases

  def create_individual(self, individual_size):
    randomSelection = sample(individual_size, randint(0, individual_size))
    individual = [0 for i in range(individual_size)]
    for i in randomSelection:
      individual[i] = 1
    return individual

  def create_population(self, individual_size, population_size):
    return [self.create_individual(individual_size) for i in range(population_size)]

  def selected(self, selection, phrase):
    selectedSents = [sent for choice, sent in zip(selection, self.summary) if choice == 1]
    for sent in selectedSents:
      if phrase in sent:
        return True
    return False

  def get_fitness(self, individual):
    if sum([self.l[i] for i in range(len(self.summary)) if individual[i] == 1]) <= self.L:
      return sum([score for (score, phrase) in self.rankedPhrases if self.selected(individual, phrase)]) + sum([(self.scores_sent[i] + self.l[i]/self.L) for i in range(len(self.summary)) if individual[i] == 1])
    else:
      return 0

  def evaluate_population(self, population):
    fitness_list = [self.get_fitness(individual) for individual in population]
    sorted_population = [individual for _, individual in sorted(zip(fitness_list, population))]
    sorted_population.reverse()
    best_individuals = sorted_population[: selection_size]
    best_individuals_stash.append(best_individuals[0])
    return best_individuals

  def crossover(self, parent_1, parent_2):
      child = {}
      loci = [i for i in range(0, self.individual_size)]
      loci_1 = sample(loci, floor(0.5*(self.individual_size)))
      loci_2 = [i for i in loci if i not in loci_1]
      chromosome_1 = [[i, parent_1[i]] for i in loci_1]
      chromosome_2 = [[i, parent_2[i]] for i in loci_2]
      child.update({key: value for (key, value) in chromosome_1})
      child.update({key: value for (key, value) in chromosome_2})
      return [child[i] for i in loci]

  def mutate(self, individual):
      loci = [i for i in range(0, self.individual_size)]
      no_of_genes_mutated = floor(self.probability_of_gene_mutating * self.individual_size)
      loci_to_mutate = sample(loci, no_of_genes_mutated)
      for locus in loci_to_mutate:
          if individual[locus] = 0:
            individual[locus] = 1
          else:
            individual[locus] = 0
      return individual

  def get_new_generation(self, selected_individuals):
      parent_pairs = [sample(selected_individuals, 2) for i in range(self.population_size)]
      offspring = [crossover(pair[0], pair[1]) for pair in parent_pairs]
      offspring_indices = [i for i in range(self.population_size)]
      offspring_to_mutate = sample(
          offspring_indices,
          floor(self.probability_of_individual_mutating * self.population_size)
      )
      mutated_offspring = [[i, self.mutate(offspring[i])] for i in offspring_to_mutate]
      for child in mutated_offspring:
          offspring[child[0]] = child[1]
      return offspring

  def check_termination_condition(self, best_individual_fitness):
    if (best_individual_fitness >= self.THRESHOLD) or (self.generation_count == self.max_generations):
      return True
    else:
      return False

  def getSummary(self):
    while self.termination == False:
      current_best_individual = self.get_fitness(self.best_individuals_stash[-1])
      best_individuals = self.evaluate_population(self.current_population)
      self.current_population = self.get_new_generation(best_individuals)
      self.termination = self.check_termination_condition(current_best_individual)
      self.generation_count += 1
      
    print('best selection: ', self.best_individuals_stash[-1])
    return self.best_individuals_stash[-1]
