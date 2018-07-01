 /*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package rsa;

import java.math.BigInteger;
import java.util.Random;

/**
 *
 * @author weiss
 */

class ExtEuclides {
    BigInteger d, x, y;

    public ExtEuclides(BigInteger d, BigInteger x, BigInteger y) {
        this.d = d;
        this.x = x;
        this.y = y;
    }
    
    @Override
    public String toString (){
        return (new String("D: " + this.d + " X: " + this.x + " Y: " + this.y));
    }
}

public class RSA {
    
    public static BigInteger expModular (BigInteger base, BigInteger exp, BigInteger mod){
        BigInteger res = BigInteger.ONE;
        while(exp.compareTo(BigInteger.ZERO) == 1){
            if(exp.mod(new BigInteger("2")).compareTo(BigInteger.ONE) == 0){
                res = res.multiply(base).mod(mod);
            }
            base = base.multiply(base).mod(mod);
            exp = exp.divide(new BigInteger("2"));
        }
        return res;
    }
    
    public static BigInteger euclides (BigInteger a, BigInteger b){
        if(b.compareTo(BigInteger.ZERO) == 0){
            return a;
        }
        return euclides(b, a.mod(b));
    }
    
    public static ExtEuclides extEuclides (BigInteger a, BigInteger b){
        if(b.compareTo(BigInteger.ZERO) == 0){
            return (new ExtEuclides(a, BigInteger.ONE, BigInteger.ZERO));
        }
        ExtEuclides tmp = extEuclides(b, a.mod(b));
        ExtEuclides res = new ExtEuclides(tmp.d, tmp.y, tmp.x.subtract(a.divide(b).multiply(tmp.y)));
        return res;
    }
    
    public static boolean witness(BigInteger candidato){
        Random rand = new Random();
        BigInteger bigRandom = new BigInteger(candidato.bitLength(), rand);
        bigRandom = bigRandom.min(candidato.subtract(BigInteger.ONE));
        bigRandom = bigRandom.max(new BigInteger("2"));
        BigInteger res = expModular(bigRandom, candidato.subtract(BigInteger.ONE), candidato);
        if(res.compareTo(BigInteger.ONE) == 0){
            return true;
        }
        return false;
    }
    
    public static boolean fermat(BigInteger candidato, int tentativas){
        for(int i = 0; i < tentativas; i++){
            if(!witness(candidato)){
                return false;
            }
        }        
        return true;
    }
    
    public static BigInteger modLinSolver(BigInteger a, BigInteger b, BigInteger n){
        ExtEuclides ret = extEuclides(a, n);
        BigInteger x0 = null;
        if(b.mod(ret.d).compareTo(BigInteger.ZERO) == 0){
            x0 = ret.x.multiply(b.divide(ret.d)).mod(n);
        }
        return x0;
    }
    
    public static BigInteger[] PQ(int numBits){
        BigInteger[] ret = new BigInteger[2];
        Random rand = new Random();
        boolean flag = false;
        while(!flag){
            ret[0] = new BigInteger(numBits, rand);
            if(fermat(ret[0], 100) == true){
                flag = true;
            }
        }
        flag = false;
        while(!flag){
            ret[1] = new BigInteger(numBits, rand);
            if(fermat(ret[1], 100) == true && euclides(ret[0], ret[1]).compareTo(BigInteger.ONE) == 0){
                flag = true;
            }
        }
        return ret;
    }
    
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        
        System.out.println("Expo modular 2^10: " + expModular(new BigInteger("2"), new BigInteger("10"), new BigInteger("10000000007")));
        System.out.println("Euclides 128 64: " + euclides(new BigInteger("128"), new BigInteger("64")));
        ExtEuclides teste = extEuclides(new BigInteger("1914"), new BigInteger("899"));
        System.out.println("ExtEuclides 1914 e 899: " + teste);
        System.out.println("Fermat para 1000000007: " + fermat(new BigInteger("1000000011"), 100));
        System.out.println("ModLinSolve 227 e 198640: " + modLinSolver(new BigInteger("227"), BigInteger.ONE, new BigInteger("198640")));
        BigInteger[] ret = PQ(40);
        System.out.println("Primo 1: " + ret[0] + " Primo 2: " + ret[1]);
    }
    
}