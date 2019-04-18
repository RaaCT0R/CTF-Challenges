## Challenge name:	:)
### Difficulty:	easy

### Description:
> Look at what I found! 
XUBdTFdScw5XCVRGTglJXEpMSFpOQE5AVVxJBRpLT10aYBpIVwlbCVZATl1WTBpaTkBOQFVcSQdH

### Solution:

What we see is like base64, so we decode it.

    import base64

	c = 'XUBdTFdScw5XCVRGTglJXEpMSFpOQE5AVVxJBRpLT10aYBpIVwlbCVZATl1WTBpaTkBOQFVcSQdH'
	c = base64.b64decode(c)

**Output**
	
    ']@]LWRs\x0eW\tTFN\tI\\JLHZN@N@U\\I\x05\x1aKO]\x1a`\x1aHW\t[\tV@N]VL\x1aZN@N@U\\I\x07G'

So we got something meaningless.
Here we need an encryption system that change hidden characters to word. The difficulty is easy, so it should be an easy one. I guess it's a repeating-XOR. We know flag starts with 'gigem{', so lets XOR 6 starting bytes with this string.

    def xorbyte(s, key):
	    key = key * (len(s) // len(key) + 1)
	    output = ''
	    for i in range(len(s)):
	        output += chr(ord(s[i]) ^ ord(key[i]))
	    return output
	    
	xorbyte(c[:6], 'gigem{'

**Output**

    ':):):)'
   
Repeats of ':)', it seems we got the key! Lets XOR all bytes to ':)'.

    xorbyte(c, ':)')
  **Output**
  

    "gigem{I'm not superstitious, but I am a little stitious.}"


