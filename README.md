<h1>Voronoi Art</h1>
<h6>Erik Blix and Anthony Mozloom</h6>
<br>
<h3>Project Description</h3>
<p>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; The Voronoi Art Project is a Python-based genetic algorithm that uses Voronoi diagrams to replicate images it is provided. This approach combines genetic algorithms, which mimic the process of natural selection, with Voronoi diagrams, a spatial partitioning technique. 

</p>
<h3>How it works</h3>
<p>

1. **Initialization**: The algorithm starts with a population of randomly generated Voronoi diagrams.

2. **Evaluation**: Each individual in the population is evaluated by comparing the generated Voronoi diagram's appearance to the target image using the imgcompare library.

3. **Selection**: Individuals are selected for reproduction based on their fitness, with better-performing individuals having a higher chance of being selected.

4. **Crossover**: Pairs of selected individuals undergo crossover to create a new generation of Voronoi diagrams.

5. **Mutation**: Random mutations are applied to the new generation, introducing small changes in position or color of the points.

6. **Repeat**: Steps 2-5 are repeated for multiple generations, refining the polygons to better replicate the target image (in testing this took about 10,000 generations).
</p>

<h3>Usage</h3>
<p>

1. **Import your Image**:

    - Add the image you want to replicate to the 'Testing Images' folder.

2. **Update Filepath in darwin.py**:

    - Open the 'darwin.py' file and locate the line where the filepath for the target image is specified at the bottom.
    - Update the filename to match the name of your target image in the 'Testing Images' folder.

    ```python
    # Update the filename to match your target image
    original_image_filename = 'original_image.png'

    ```

3. **Run the Algorithm**:

    - Open a terminal or command prompt and navigate to the project directory.
    - Run the following command:

    ```bash
    python3 darwin.py
    ```

4. **Monitor Progress**:

    - Open the 'GAOutput.txt' file to observe the progress of the genetic algorithm.
    - This file logs information about each generation, including generation number, average fitness, best fitness, and the string representation of the best individual, in that order.

5. **Customize Algorithm Behavior**:

    - Open the 'darwin.py' file to customize the algorithm behavior:
        - In the `evolve` method, you can change whether or not the genes will divide and replicate.
        - In the `createChildren` method, you can change whether the mutation rate decrements at a certain point.

</p>

<h3>Credits</h3>
<h6>This project was inspired by the work described in the following blog post: </h6>

* **Title**: Minimalist Art Using a Genetic Algorithm
* **Author**: Sebastian Proost
* **Link**: https://blog.4dcu.be/programming/2020/02/10/Genetic-Art-Algorithm-2.html

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The original work addressed challenges in achieving a specific style of minimalist artwork using a genetic algorithm. The author's exploration led to the use of Voronoi diagrams, offering a unique solution and achieving closer alignment with the desired artistic outcome. Some of the code in our project was taken from this article.