10 steps to becoming a better programmer
========

[raw article](http://www.wildbunny.co.uk/blog/2012/11/01/10-steps-to-becoming-a-better-programmer/), I removed the code

<!-- 
[comment]: <> (This is a comment, it will not be included)
[comment]: <> (in  the output file unless you use it in)
[comment]: <> (a reference style link.) 
[^_^]:
    b
-->

I wanted to cover 10 of the things I've learned over the years being a professional programmer that really helped me improve the quality of my code and my overall productivity.

## 1. Never ever duplicate code
Avoid duplicating code at all costs. If you have a common code segment used in a few different places, refactor it out into its own function. Code duplication causes confusion among your colleagues reading your code, it causes bugs down the line when the duplicated segment is fixed in one location and not the others and it bloats the size of your code-base and executable. With modern languages its become possible to get really good at this, for example here is a pattern that used to be hard to solve before delegates and lambdas came along:

/// <summary>
/// Some function with partially duplicated code
/// </summary>
void OriginalA()
{
	DoThingsA();
 
	// unique code
 
	DoThingsB();
}
 
/// <summary>
/// Another function with partially duplicated code
/// </summary>
void OriginalB()
{
	DoThingsA();
 
	// unique code
 
	DoThingsB();
}
But now we can refactor the shared part of both functions and rewrite using a delegate:

/// <summary>
/// Encapsulate shared functionality
/// </summary>
/// <param name="action">User defined action</param>
void UniqueWrapper(Action action)
{
	DoThingsA();
 
	action();
 
	DoThingsB();
}
 
/// <summary>
/// New implmentation of A
/// </summary>
void NewA()
{
	UniqueWrapper(() =>
	{
		// unique code
	});
}
 
/// <summary>
/// New implementation of B
/// </summary>
void NewB()
{
	UniqueWrapper(() =>
	{
		// unique code
	});
}
2. Notice when you start distracting yourself
When you find yourself flicking to facebook or twitter instead of working on a problem its often a sign that you need to take a short break. Go grab a coffee away from your desk and talk to your colleagues for 5 minutes or so. Even though this seems counter intuitive, you will be more productive in the long run.

3. Don't rush the solution out the door
When under pressure to produce a solution to a problem, or to fix a bug, its very easy to get carried away and find yourself rushing, or even missing out your usual crucial testing cycle completely. This can often result in more problems and will make you look less professional in the eyes of your boss and colleagues.

4. Test your finished code
You know what your code is supposed to do, and you've likely tested that it works, but you really need to prove it. Analyse all the potential edge cases and make a test which confirms that your code performs as expected under all possible conditions. If there are parameters, send values outside of the expected range. Send null values. If you can, show your code to a colleague and ask them to break it. Unit testing is a formalised approach to this.

5. Code review
Before you promote your code into source control, sit down with a colleague and explain exactly what your change does. Often just by doing this you'll recognise mistakes in your own code without your colleague saying a word. It's much, much more effective than just reviewing your own work.

6. Write less code
If you find yourself writing a lot of code to do something simple, you're probably doing it wrong. A good example is the lowly boolean:

if (numMines > 0)
{
   enabled=true;
}
else
{
   enabled=false;
}
When you could just write:

enabled = numMines > 0;
The less code you write the better. Less to debug, less to refactor, less to go wrong. Use with moderation; readability is just as important, you don't want to make your code less readable by doing this.

7. Strive for elegant code
Elegant code is highly readable and solves the problem at hand with the smallest amount of code and machine action possible. Its quite difficult to achieve elegant code in all circumstances but after programming for a while you start to get a feel for what it looks like. Elegant code cannot be improved by refactoring anything. It makes you happy to look at it. You are proud of it. For example here is what I consider to be an elegant way of computing the area of a convex polygon:

static public double GetConvexPolygonArea(Vector2[] vertices)
{
	double area = 0;
	for (int i = 0; i < vertices.Length; i++)
	{
		Vector2 P0 = vertices[i];
		Vector2 P1 = vertices[(i + 1) % vertices.Length];
 
		area += P0.Wedge(P1);
	}
 
	return area / 2;
}
8. Write self documenting code
Comments are a very important part of programming for obvious reasons, but self documenting code can be even better because it makes it possible to understand code just by reading it. Function and variable names can often be deftly chosen so that when put together with the language semantics the code becomes readable even to non programmers. For example:

void DamagePlayer(Player player, int damageAmount)
{
	if (!player.m_IsInvincible && !player.m_IsDead)
	{
		player.InflictDamage( damageAmount );
	}
}
Self documenting code is not a substitute for comments. Use comments to describe 'why', self documenting code describes 'what'.

9. Don't use magic numbers
Numbers just inserted into the code are bad practice because there is nothing to describe what they represent. This is compounded by duplication; where the same number is used in multiple different places in the code. One will get changed and the others missed leading to bugs. Always use a named constant to describe the value you want to represent, even if it is only used in one place.

10. Don't do manual labour
Humans are very good at making mistakes when doing a series of actions. If you have a build deployment process which is more than one step long, you're doing it wrong. Automate as much as possible, reduce the chance of human error. This is especially important with tasks which you perform a lot.

11. Avoid premature optimisation
When you start optimising part of your already functioning code you risk breaking the functionality. Optimisation should only be performed in response to performance analysis, hopefully carried out towards the end of a project. Optimising before this analysis stage wastes time and can introduce bugs.

Ok, well I said 10, but you get an extra one for free!

That's it for now, I hope these little points will help you improve your programming and development process.

Until next time, have fun!

Cheers, Paul.
