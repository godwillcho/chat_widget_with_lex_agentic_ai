<script type="text/javascript">
    // TODO: Replace with your staging Amazon Connect widget script
    // Get this from: Amazon Connect Console → Channels → Chat widgets → Your widget → "Show security key"
    // Copy the entire <script>...</script> block and paste it here

    (function(w, d, x, id){
        s=d.createElement('script');
        s.src='https://YOUR-INSTANCE.my.connect.aws/connectwidget/static/amazon-connect-chat-interface-client.js';
        s.async=1;
        s.id=id;
        d.getElementsByTagName('head')[0].appendChild(s);
        w[x] =  w[x] || function() { (w[x].ac = w[x].ac || []).push(arguments) };
    })(window, document, 'amazon_connect', 'YOUR-WIDGET-ID-HERE');
    amazon_connect('snippetId', 'YOUR-SNIPPET-ID-HERE');
    amazon_connect('supportedMessagingContentTypes', [ 'text/plain', 'text/markdown' ]);
</script>
