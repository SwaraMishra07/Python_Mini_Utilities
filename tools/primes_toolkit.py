#!/usr/bin/env python3
"""
Prime Number Toolkit CLI
Usage: python primes_toolkit.py {gen|factor|isprime} [args]

Subcommands:
  gen N         - Generate primes up to N using Sieve of Eratosthenes
  factor N      - Factorize N via trial division
  isprime N     - Check if N is prime (optimized for large N)
"""

import argparse
import sys
import math

def sieve_of_eratosthenes(n):
    """Generate list of primes up to n using Sieve."""
    if n < 2:
        return []
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(math.sqrt(n)) + 1):
        if is_prime[i]:
            for j in range(i*i, n+1, i):
                is_prime[j] = False
    return [i for i in range(2, n+1) if is_prime[i]]

def factorize(n):
    """Factorize n via trial division up to sqrt(n). Returns sorted list of prime factors."""
    if n < 2:
        return []
    factors = []
    # Check 2 separately
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    # Odd factors up to sqrt(n)
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        while n % i == 0:
            factors.append(i)
            n //= i
    if n > 1:
        factors.append(n)
    return factors

def is_prime_optimized(n):
    """Check if n is prime: 6k±1 + Miller-Rabin for large n."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    
    # 6k±1 optimization
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    
    # Miller-Rabin for large n (deterministic up to 2^64 with these witnesses)
    if n < 2**64:
        witnesses = [2, 3, 5, 7, 11, 13, 17, 23, 29, 31, 37]
    else:
        witnesses = [2, 3, 5, 7, 11, 13, 17]  # Sufficient for most cases
    return miller_rabin(n, witnesses)

def miller_rabin(n, witnesses):
    """Miller-Rabin primality test."""
    # Write n-1 as 2^s * d
    s, d = 0, n - 1
    while d % 2 == 0:
        s += 1
        d //= 2
    
    for a in witnesses:
        if a >= n:
            break
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def main():
    parser = argparse.ArgumentParser(description="Prime Number Toolkit CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands", required=True)
    
    # gen subparser
    gen_parser = subparsers.add_parser("gen", help="Generate primes up to N")
    gen_parser.add_argument("N", type=int, help="Upper limit")
    
    # factor subparser
    factor_parser = subparsers.add_parser("factor", help="Factorize N")
    factor_parser.add_argument("N", type=int, help="Number to factorize")
    
    # isprime subparser
    isprime_parser = subparsers.add_parser("isprime", help="Check if N is prime")
    isprime_parser.add_argument("N", type=int, help="Number to check")
    
    args = parser.parse_args()
    
    if args.command == "gen":
        if args.N > 10**7:  # Reasonable limit for CLI
            print("Error: N too large (max 10M for performance)", file=sys.stderr)
            sys.exit(1)
        primes = sieve_of_eratosthenes(args.N)
        print("Primes up to {} ({} primes):".format(args.N, len(primes)))
        print(" ".join(map(str, primes)))
    
    elif args.command == "factor":
        factors = factorize(args.N)
        if not factors:
            print("1 (no prime factors)")
        else:
            print("{} = {}".format(args.N, " × ".join(map(str, factors))))
    
    elif args.command == "isprime":
        result = is_prime_optimized(args.N)
        print("Yes" if result else "No")

if __name__ == "__main__":
    main()
