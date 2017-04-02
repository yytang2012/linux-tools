cdf  <-
function(array, return.cdf = F, add = F, type = "l", pch, ...)
{
	# Plot a CDF of the data in "array".  If return.cdf is true,
	# then the points are returned as a list.  If add is true,
	# then the lines (or points) are added to an existing plot.
        x <- sort(array)
        y <- ppoints(array)
        if(return.cdf)
                list(x = x, y = y)
        else if(add) {
                if(missing(pch))
                        lines(x, y, type = type, ...)
                else points(x, y, pch = pch, ...)
        }
        else plot(x, y, type = type, ...)
}

lcdf <-
function(array, return.cdf = F, fit = F, add = F, reg = F, ...)
{
	# Returns a log complementary distribution plot of "array",
	# optionally fitting a line (fit=T) using least squares
	# or robust regression (reg=T).
        x <- sort(array)
        y <- log10(1 - ppoints(x))
        if(return.cdf)
                list(x = x, y = y)
        else {
                if(add)
                        lines(x, y, type = "l", ...)
                else plot(x, y, type = "l", ...)
                if(fit) {
                        if(reg)
                                r <- rreg(x, y)
                        else r <- lsfit(x, y)
                        abline(r)
                        list(Coefficient=r$coef,Correlation=cor(x,y))
                }
        }
}

llcdf <-
function(x, ...)	# do a log-log complementary distribution plot
lcdf(log10(x), ...)

choose1 <-
function(n, k)	# computes Choose() for small n and k
factorial(n)/(factorial(k) * factorial(n - k))

choose2 <-
function(n, k)	# computes Choose() for arbitrary n and k
exp(log.choose(n, k))

log.choose <-
function(n, k)
lgamma(n + 1) - (lgamma(k + 1) + lgamma(n - k + 1))

collect <-
function(array, func, ...)
{
	# Returns a vector corresponding to applying function "func"
	# to each element of "array".
        result <- c()
        for(i in array)
                result <- c(result, func(i, ...))
        result
}

ac <-
function(x, max.lag, ...)
{
	# Computes the autocorrelation of x up to lag max.lag
        if(missing(max.lag)) {
                n <- len(x)
                max.lag <- 2^ceiling(lg(n + 1)) - n
                cat("length = ", n, ", padding = ", max.lag, ", total = ",
                        n + max.lag, "\n")
        }
        x <- x - mean(x)
        x <- c(x, rep(0, max.lag))
        a <- corr.fft(x, x, ...)
        a <- a[-1]/a[1]
        a[1:max.lag]
}

autocorr.simple <-
function(array, lag = 1)
{
	# Autocorrelation for one particular lag.
        l <- len(array)
        cor(array[1:(l - lag)], array[(1 + lag):l])
}

bern.to.prob <-
function(t, x, n = 20, discard = 1/4, uniform = F)
{
# Given Bernoulli observations at times t with 1/0 values x,
# divides them up into exponentially-spaced bins with roughly n
# occupants per bin and returns the corresponding probability
# of x=1 for each bin center.  Discard any bins with less than
# "discard" of n occupants.  If "uniform" is true, then the times
# are assumed to be uniformly distributed, and the binning is
# done fixed-width.
        o <- order(t)
        x <- x[o]
        t <- t[o]
        if(uniform) {
                span <- max(t) - min(t)
                num.bins <- len(t)/n
                width <- span/num.bins
                tprime <- t - min(t)
                tprime <- tprime/width
                bins <- as.integer(tprime)
        }
        else {
                lambda <- 1/mean(t)
                quantiles <- 1 - exp( - lambda * t)
                nbins <- len(t)/n
                bins <- as.integer(quantiles * nbins)
        }
        bin.boundaries <- c(bins[-1] != bins[ - len(bins)], T)
        cum.x <- cumsum(x)
        cum.n <- 1:len(x)
        bin.x <- diff(c(0, cum.x[bin.boundaries]))
        bin.n <- diff(c(0, cum.n[bin.boundaries]))
        bin.t <- (t[bin.boundaries] + c(0, t[bin.boundaries[ - len(
                bin.boundaries)]]))/2
        keep <- bin.n >= n * discard
        list(x = bin.x[keep], n = bin.n[keep], t = bin.t[keep])
}

corr.fft <-
function(x, y, pad = T)
{
	# Computes correlation of x and y using FFT.  If pad is T,
	# pads them to a power of 2 (to speed the computation).
        if(len(x) != len(y))
                stop("arguments to corr.fft must be the same length")
        n <- len(x)
        n2 <- 2^ceiling(lg(n))
        if(n != n2 && pad) {
                x <- c(x, rep(0, n2 - n))
                y <- c(y, rep(0, n2 - n))
        }
        fft.x <- fft(x)
        if(all(x == y))
                fft.y <- fft.x
        else fft.y <- fft(y)
        Re(fft(fft.x * Conj(fft.y), inverse = T))
}

aggregate.array <-
function(x, aggregation, smooth = T)
{
	# Aggregate array "x" by a factor of "aggregation".  If smooth
	# is true, then do the aggregation by averaging, otherwise by
	# adding.
        s <- c(0, cumsum(x))
        bins <- seq(1, len(x) + 1, by = aggregation)
        if(smooth)
                (s[bins[-1]] - s[bins[ - len(bins)]])/aggregation
        else s[bins[-1]] - s[bins[ - len(bins)]]
}

cum.mean <-
function(x)
{
# computes cumulative mean of an array; i.e., returns another array
# whose element i is the mean of x[1:i]
        cumsum(x)/(1:len(x))
}

peaks <-
function(x, min = F, cut = 5)
{
	# Returns the "cut" biggest (smallest, if min=T) peaks in
	# array x.
        if(min)
                x <-  - x
        n <- len(x)
        bigger.than.lhs <- x >= c( - Inf, x[1:(n - 1)])
        bigger.than.rhs <- x >= c(x[-1],  - Inf)
        pos <- seq(x)[bigger.than.lhs & bigger.than.rhs]
        pos[rev(order(x[pos]))][1:cut]
}

per <-
function(z)
{
# definition of the periodogram function
        n <- length(z)
        (Mod(fft(z))/(2 * pi * n))[1:(n %/% 2 + 1)]
}

binomial.param <-
function(total, observed, P)
{
# For a binomial distribution, returns the binomial parameter p such that
# the probability of "observed" observations or fewer out of "total"
# samples is equal to "P".
        1 - binomial.param2(total, total - observed, P)
}

binomial.param2 <-
function(total, observed, P)
{
# For a binomial distribution, returns the binomial parameter p such that
# the probability of "observed" observations or more out of "total"
# samples is equal to "P".
# Taken from p. 960, Handbook of Mathematical Functions, ed. Milton
# Abramowitz and Irene A. Segun.
        if(observed == 0) return(0)
        nu1 <- 2 * (total - observed + 1)
        nu2 <- 2 * observed
        Q <- qf(1 - P, nu1, nu2)
        nu2/(nu2 + nu1 * Q)
}

binomial.range <-
function(total, observed, conf = 0.95, compare = F)
{
# Given "observed" instances of an event out of "total" experiments,
# returns the range of possible probabilities for the event consistent
# with the given confidence.
        if(compare) conf <- 1 - 2 * sqrt(1 - conf)
        P <- 1/2 - conf/2
        p.lower <- binomial.param(total, observed, P)
        p.upper <- binomial.param2(total, observed, P)
        sort(c(p.lower, p.upper))
}

binomial.range2 <-
function(total, observed, conf = 0.95, compare = F)
{
# Given "observed" instances of an event out of "total" experiments,
# returns the range of possible probabilities for the event consistent
# with the given confidence.
        if(compare) conf <- 1 - sqrt(1 - conf)
        P <- 1/2 - conf/2
        p.lower <- binomial.param(total, observed, P)
        p.upper <- binomial.param2(total, observed, P)
        sort(c(p.lower, p.upper))
}

dbinomial <-
function(n, successes = 0:n, p = 0.5)
{
# Returns the probability of 0..n successes in n trials, each with
# independent probability p.
        choose(rep(n, len(successes)), successes) * p^successes * (1 - p)^
                (n - successes)
}

dbinomial2 <-
function(n, successes = 0:n, p = 0.5)
{
# Returns the probability of 0..n successes in n trials, each with
# independent probability p.
        log.c <- log.choose(rep(n, len(successes)), successes)
        exp(log.c + successes * log(p) + (n - successes) * log(1 - p))
}

pbinomial <-
function(n, k, p = 0.5, approx = F)
{
# Returns the probability of at most k successes in n trials, each with
# independent probability p.
        if(approx) pbinomial.approx(n, k, p) else sum(dbinomial2(n, 0:k, p))
}

pbinomial.approx <-
function(n, k, p = 0.5)
{
# Returns the approximate probability of at most k successes in n trials,
# each with independent probability p.
        q <- 1 - p
        prod <- n * q * p
        if(prod <= 25 && (prod <= 5 || p < 0.1 || p > 0.9) && min(n * p, n *
                q) <= 10)
                cat("approximating binomial with normal ill-advised for n =",
                        n, "p =", p, "q =", q, "\n")
        mean <- n * p
        sigma <- sqrt(n * p * q)
        pnorm(k, mean, sigma)
}

pbinomial2 <-
function(n, k, p = 0.5)
{
# Returns the probability of at least k successes in n trials, each with
# independent probability p.
        if(k == 0) 1 else 1 - pbinomial(n, k - 1, p)
}

order.prob <-
function(m, n, k)
{
# Probability that when (m+n) elements are sorted, the first
# k will be from m
        choose(m, k)/choose(m + n, k)
}

fisher  <-
function(n1, k1, n2, k2, alpha = 0.05)
{
# Returns true if k1 observations out of n1 is consistent with
# confidence 1-alpha with observing k2 observations out of n2,
# using Fisher's exact test.
        n <- n1 + n2
        k <- k1 + k2
        prob.below <- sum(fisher1(n, k, n1, max(0, k - n2):k1))
        prob.above <- sum(fisher1(n, k, n1, min(n1, k):k1))
        min(prob.below, prob.above) > alpha/2
}

fisher1 <-
function(n, k, n1, k1)
{
# Returns the probability of observing exactly k1 instances out of n1 samples,

# given a total of n samples and k observations of property K.
# Done using Fisher's exact test, per p. 484 of "Mathematical Statistics
# and Data Analysis," 2nd edition, by John Rice.
        exp((log.choose(n1, k1) + log.choose(n - n1, k - k1)) - log.choose(
                n, k))
}

exp.A2 <-
function(x, quiet = F, plot = F, return.sig = F, do.round = T, ...)
{
	# Computes Anderson-Darling on fitting an exponential to the
	# given array.
        x <- sort(x)
        m <- mean(x)
        z <- pexp(x/m)
        val <- A2(z)
        sig <- A2.exp.significance(val, len(x))
        if(plot)
                lines(x, z, ...)
        if(return.sig)
                return(list(sig = if(do.round) round.sig(sig) else sig, p1 = m,
                        p2 = 0, num = len(x)))
        if(!quiet)
                print(paste(sig, "% significance", sep = ""))
        val
}

A2.exp.significance <-
function(val, n)
{
	# Significance levels for different Anderson-Darling results when
	# applied to exponential fits.
        val <- val * (1 + 0.6/n)
        levels <- c(0.736, 0.816, 0.916, 1.062, 1.321, 1.591, 1.959)
        sig <- max(c(0.25, 0.2, 0.15, 0.1, 0.05, 0.025, 0.01)[val <= levels])
        if(is.na(sig))
                sig <- 0
        sig * 100
}

norm.A2  <-
function(array, plot = F, return.sig = F, ...)
{
	# Computes Anderson-Darling on fitting a Gaussian to the
	# given array.
        array <- sort(array)
        n <- len(array)
        m <- mean(array)
        s <- stddev(array)
        z <- pnorm(array, m, s)
        if(plot)
                lines(array, z, ...)
        val <- A2(z)
        val <- val * (1 + 0.75/n + 2.25/n2)
        val
        levels <- c(0.341, 0.47, 0.561, 0.631, 0.752, 0.873, 1.035)
        sig <- max(c(0.5, 0.25, 0.15, 0.1, 0.05, 0.025, 0.01)[val <= levels])
        if(is.na(sig))
                sig <- 0
        if(return.sig)
                return(list(sig = round.sig(sig * 100), p1 = m, p2 = s, num = n
                        ))
        print(paste("Significance =", sig * 100, "%"))
        val
}

A2 <-
function(z)
{
	# Raw Anderson-Darling statistic.
        n <- length(z)
        i <- seq(z)
        (-n) - (1/n) * sum((2 * i - 1) * log(z) + (2 * n + 1 - 2 * i) *
                log(1 - z))
}

factorial <-
function(n)
gamma(n + 1)

len <-
# a handy synonym for "length"
length

lg <-
function(x)
log(x, base = 2)

lplot <-
function(...)	# plot using lines rather than points
plot(..., type = "l")

min.gold <-
function(f, a, b, c, tol = 1e-06, max.steps = Inf, ...)
{
# Finds a local minima of f lying in (a,c), given that a < b < c and
# f(b) < f(a), f(b) < f(c), using golden section search (Numerical Recipes).
# "tol" is the tolerance on x; "max.steps" is an upper bound on the number
# of evaluations of f that we do.
        golden <- 0.61803399
        golden1 <- 1 - golden
        if(c - b > b - a)
                d <- b + golden1 * (c - b)
        else {
                d <- b
                b <- b - golden1 * (b - a)
        }
        fb <- f(b, ...)
        fd <- f(d, ...)
        steps <- 2
        while(c - a > tol && steps < max.steps) {
                if(fd < fb) {
                        a <- b
                        b <- d
                        d <- golden * b + golden1 * c
                        fb <- fd
                        fd <- f(d, ...)
                }
                else {
                        c <- d
                        d <- b
                        b <- golden * d + golden1 * a
                        fd <- fb
                        fb <- f(b, ...)
                }
                steps <- steps + 1
        }
        if(fb < fd)
                list(x = b, f = fb, steps = steps, tol = c - a)
        else list(x = d, f = fd, steps = steps, tol = c - a)
}



run.lengths <-
function(x)
{
# Returns the lengths of all of the runs in x, which is assumed
# to be a boolean array of T's for run bodies and F's for gaps
# between runs.
        x.aug <- c(F, x, F)
        n <- len(x.aug)
        run.start <- x.aug[-1] > x.aug[ - n]
        run.end <- x.aug[ - n] > x.aug[-1]
        index <- seq(n - 1)
        index[run.end] - index[run.start]
}

power.spectrum <-
function(x)
{
	# Returns the power spectrum of x.
        ft <- fft(x)
        ft <- ft[1:(len(ft)/2 + 1)][-1]
        abs(ft)
}

psplot   <-
function(x, is.ps = F, smooth = F, frac = 0.1, ...)
{
	# Plots the power spectrum of x, or, if is.ps is true,
	# plots an already-computed power spectrum.  Adds fits
	# to the lower frac frequencies.
        if(!is.ps)
                x <- power.spectrum(x)
        if(smooth) {
                if(smooth == 1)
                        smooth <- 4
                x <- aggregate.array(x, smooth)
        }
        pplot(x, log = "xy", xlab = "Frequency", ylab = "Power", ...)
        # llplot(x, ...)
        collect(frac, function(frac, x)
        {
                fit <- power.fit(x, stop = len(x) * frac)
        # lines(log10(fit$x), log10(fit$y))
                lines(fit$x, fit$y)
                fit$power
        }
        , x)
}

pplot <-
function(...)	# handy function for plotting dot-sized points
plot(..., pch = ".")

pps <-
function(...)
{
	# Generates a postscript figure with minimal surround
	# whitespace (used for cramming into overlong papers).
        ps(...)
        par(mgp = c(1, 0, 0))
        par(mar = c(3, 2, 1, 1))
        par(tck = 0.02)
}

read.count  <-
function(file)	# an example of reading columnar data from a file
read.table(file, col = c("x", "y", "cnt"))

reduce <-
function(array, reduce.init, application.func, reduction.func, ...)
{
	# For each element of array, applies application.func to transform
	# the element, then reduction.func to the accumulated result and
	# the transformed element to get the new accumulated result.
        result <- reduce.init
        for(i in array)
                result <- (reduction.func)(result, (application.func)(i, ...),
                        ...)
        result
}

remove.na <-
function(array)	# removes missing data from an array
array[!is.na(array)]

rpareto <-
function(n, a, k)
# generates n Pareto-distributed variates with shape parameter a and
# minimum value k.
k/(runif(n)^(1/a))

scale.array <-
function(x, new.mean, new.stddev)
{
# apply a linear transformation to x so that it has the given mean
# and standard deviation
        old.mean <- mean(x)
        old.stddev <- stddev(x)
        scale.adjust <- new.stddev/old.stddev
        offset.adjust <- new.mean - scale.adjust * old.mean
        x * scale.adjust + offset.adjust
}

scale.plot <-
function(x, smooth = 1, scale = 1, yzero = F, yrange, highlight, ...)
{
	# Plot x after scaling it by a factor of "smooth".
        x <- aggregate.array(x, smooth, smooth = F)
        if(missing(yrange))
                yrange <- range(x)
        else yrange <- yrange * smooth
        if(yzero)
                lplot((1:len(x)) * scale, x, ylim = c(0, max(x) * 1.05), ...)

        else lplot((1:len(x)) * scale, x, ylim = yrange, ...)
        if(!missing(highlight)) {
                start <- ceiling(highlight[1]/smooth)
                n <- highlight[2]/smooth
                stop <- floor(start + n - 1)
                region <- seq(start, stop, len = n)
                polygon(c(start, region, stop) * scale, c(0, x[region], 0))
        }
}

spaste   <-
function(...)
# Handy function for pasting together strings with no separator between them.
paste(..., sep = "")

spikes <-
function(source, num = 100)
{
	# Return list of each element in source that occurs more than "num"
	# times, along with the count of how often it occurs.
        x <- uniq.count(source)
        mask <- x$counts > num
        if(sum(mask) == 0)
                c()
        else matrix(c(x$x[mask], x$counts[mask]), sum(mask), 2)
}

stddev <-
function(array)
{
        sqrt(var(array))
}

tail   <-
function(x, tail = 5, upper = T)
{
	# Returns the upper (lower) "tail"% tail
        if(upper)
                x[x >= quantile(x, 1 - tail/100)]
        else x[x <= quantile(x, tail/100)]
}

truncate.to.multiple <-
function(x, multiple)
{
# Round x down to the nearest multiple of "multiple".
        x - (x %% multiple)
}

uniq.count <-
function(x)
{
	# Returns the different elements of x and how often they occur.
        counts <- table(x)
        list(x = as.integer(dimnames(counts)[[1]]), counts = as.integer(
                counts))
}

vifunc   <-
function()
# Begins editing a new function.
vi(function(x)
{
}
)

xyline <-
function(x, y, slope)
# Plots a line that passes through (x,y) with the given slope.
abline(y - slope * x, slope)