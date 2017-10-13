<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">

<xsl:for-each select="output">
R=Rank S=Score (Percentage)
<xsl:text>
</xsl:text>
</xsl:for-each>

<!--<xsl:for-each select="output/weights/feat">-->
<!--<xsl:value-of select="." />:<xsl:value-of select="./@weight" />-->
<!--<xsl:text>-->
<!--</xsl:text>-->
<!--</xsl:for-each>-->


<xsl:for-each select="output/ties/tie/chi">
<xsl:variable name="begA">
<xsl:value-of select="number(./wA/@begA)"/>
</xsl:variable>

<xsl:variable name="endA">
<xsl:value-of select="number(./wA/@endA)"/>
</xsl:variable>

<xsl:variable name="begD">
<xsl:value-of select="number(./wA/@begD)"/>
</xsl:variable>

<xsl:variable name="endD">
<xsl:value-of select="number(./wA/@endD)"/>
</xsl:variable>

<xsl:variable name="begB">
<xsl:value-of select="number(./wB/@begB)"/>
</xsl:variable>

<xsl:variable name="endB">
<xsl:value-of select="number(./wB/@endB)"/>
</xsl:variable>

<xsl:variable name="begC">
<xsl:value-of select="number(./wB/@begC)"/>
</xsl:variable>

<xsl:variable name="endC">
<xsl:value-of select="number(./wB/@endC)"/>
</xsl:variable>

<xsl:variable name="ibeg">
<xsl:value-of select="number(./sent/@ibeg)"/>
</xsl:variable>
<xsl:variable name="iend">
<xsl:value-of select="number(./sent/@iend)"/>
</xsl:variable>
			
					====*<xsl:value-of select="./@pos" />*====+<xsl:value-of select="./@annot" />
					  
1. <xsl:text disable-output-escaping="yes">></xsl:text><xsl:value-of select="./wA" />
<xsl:text disable-output-escaping="yes"> ></xsl:text><xsl:value-of select="./wB" />
2. <xsl:value-of select="./extract" />
3. <xsl:value-of select="substring(./sent,0,$begA - $ibeg+1)"/>{<xsl:value-of select="substring(./sent,$begA+1 - $ibeg,$endA - $begA)"/>}<xsl:value-of select="substring(./sent,$endA - $ibeg+1,$begB - $endA)"/>{<xsl:value-of select="substring(./sent,$begB+1 - $ibeg,$endB - $begB)"/>}<xsl:value-of select="substring(./sent,$endB - $ibeg+1,$begC - $endB)"/>{<xsl:value-of select="substring(./sent,$begC+1 - $ibeg,$endC - $begC)"/>}<xsl:value-of select="substring(./sent,$endC - $ibeg+1,$begD - $endC)"/>{<xsl:value-of select="substring(./sent,$begD+1 - $ibeg,$endD - $begD)"/>}<xsl:value-of select="substring(./sent,$endD - $ibeg +1,$iend - $endD + 1)"/>
4. R= <xsl:value-of select="../@rank" /> S= <xsl:value-of select="format-number(../@score * 100, '###,##0.00')"/>%

<!--.wA/@begA - ./sent/@ibeg-->
<xsl:text>
</xsl:text>
</xsl:for-each>
</xsl:template>
</xsl:stylesheet>
