<?xml version="1.0" encoding="UTF-8" ?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <html>
        <head>
            <title>DOU Vacancies</title>
            <meta charset="UTF-8"/>
            <meta name="viewport" content="width=device-width, initial-scale=1"/>
        <!--===============================================================================================-->
            <link rel="icon" type="image/png" href="html_styles/images/icons/favicon.ico"/>
        <!--===============================================================================================-->
            <link rel="stylesheet" type="text/css" href="html_styles/vendor/bootstrap/css/bootstrap.min.css"/>
        <!--===============================================================================================-->
            <link rel="stylesheet" type="text/css" href="html_styles/fonts/font-awesome-4.7.0/css/font-awesome.min.css"/>
        <!--===============================================================================================-->
            <link rel="stylesheet" type="text/css" href="html_styles/vendor/animate/animate.css"/>
        <!--===============================================================================================-->
            <link rel="stylesheet" type="text/css" href="html_styles/vendor/select2/select2.min.css"/>
        <!--===============================================================================================-->
            <link rel="stylesheet" type="text/css" href="html_styles/vendor/perfect-scrollbar/perfect-scrollbar.css"/>
        <!--===============================================================================================-->
            <link rel="stylesheet" type="text/css" href="html_styles/css/util.css"/>
            <link rel="stylesheet" type="text/css" href="html_styles/css/main.css"/>
        <!--===============================================================================================-->
        </head>
        <body>
            <div class="limiter">
                <div class="container-table100">
                    <div class="wrap-table100">
                        <div class="table100">
                            <table>
                                <thead>
                                    <tr class="table100-head">
                                        <th class="column1">ID</th>
                                        <th class="column2">Vacancy position</th>
                                        <th class="column3">Company</th>
                                        <th class="column4">Cities</th>
                                        <th class="column5">Info</th>
                                        <th class="column6">Remote option</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <xsl:for-each select="vacancy-list/vacancy">
                                        <tr>
                                            <td class="column1"><xsl:value-of select="@id"/></td>
                                            <td class="column2"><xsl:value-of select="name"/></td>
                                            <td class="column3"><xsl:value-of select="company"/></td>
                                            <td class="column4"><xsl:apply-templates select="cities"/></td>
                                            <td class="column5"><xsl:value-of select="info"/></td>
                                            <td class="column6"><xsl:value-of select="remote"/></td>
                                        </tr>
                                    </xsl:for-each>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        <!--===============================================================================================-->
            <script src="html_styles/vendor/jquery/jquery-3.2.1.min.js"></script>
        <!--===============================================================================================-->
            <script src="html_styles/vendor/bootstrap/js/popper.js"></script>
            <script src="html_styles/vendor/bootstrap/js/bootstrap.min.js"></script>
        <!--===============================================================================================-->
            <script src="html_styles/vendor/select2/select2.min.js"></script>
        <!--===============================================================================================-->
            <script src="html_styles/js/main.js"></script>
        </body>
        </html>
    </xsl:template>

    <xsl:template match="cities">
        <xsl:for-each select=".">
            <p><xsl:value-of select="city"/></p><br/>
        </xsl:for-each>
    </xsl:template>

</xsl:stylesheet>